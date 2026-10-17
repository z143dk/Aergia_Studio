import os
import json
import math
from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='templates', static_folder='static')

RELICS_FILE = os.path.join(os.path.dirname(__file__), 'relics.json')
STATE_FILE = os.path.join(os.path.dirname(__file__), 'player_state.json')

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    state = load_json(STATE_FILE)
    return jsonify(state)

@app.route('/api/jump', methods=['POST'])
def jump():
    req = request.json
    lat = float(req.get('lat', 0.0))
    lon = float(req.get('lon', 0.0))
    era = req.get('era', '')

    state = load_json(STATE_FILE)
    relics_data = load_json(RELICS_FILE)

    # Validate Sync and Vitality
    if state['stats']['temporal_sync'] <= 10:
        return jsonify({'error': 'Temporal Sync too low! Sleep at the safehouse first.'}), 400
    
    # Deduct jump cost
    state['stats']['temporal_sync'] = max(0, state['stats']['temporal_sync'] - 15)
    state['stats']['notoriety'] = min(100, state['stats']['notoriety'] + 5)
    
    found_relic = None
    distance = None
    unlocked = False
    missing_tool = None

    # Scan for relics matching current coordinates
    for key, relic in relics_data['relics'].items():
        if key in state['vault']:
            continue # Already found
            
        dist = haversine(lat, lon, relic['coords']['lat'], relic['coords']['lon'])
        
        # Check range limit (e.g. 50 km default; 150 km with spyglass_of_antiquity)
        max_range = 150.0 if 'spyglass_of_antiquity' in state['inventory'] else 50.0
        
        if dist <= max_range:
            distance = dist
            # Must be closer to actually extract (e.g. 5 km)
            if dist <= 5.0:
                # Check tools
                has_tools = all(tool in state['inventory'] for tool in relic['required_tools'])
                if has_tools:
                    found_relic = key
                    unlocked = True
                    state['vault'].append(key)
                else:
                    found_relic = key
                    missing_tool = relic['required_tools'][0]
            break

    save_json(STATE_FILE, state)

    response = {
        'state': state,
        'distance': distance,
        'unlocked': unlocked,
        'missing_tool': missing_tool,
        'relic_name': relics_data['relics'][found_relic]['name'] if found_relic else None,
        'lore': relics_data['relics'][found_relic]['lore'] if found_relic else None
    }
    return jsonify(response)

@app.route('/api/craft', methods=['POST'])
def craft():
    req = request.json
    result_item = req.get('result', '')

    state = load_json(STATE_FILE)
    relics_data = load_json(RELICS_FILE)

    # Find recipe
    recipe = next((r for r in relics_data['crafting_recipes'] if r['result'] == result_item), None)
    if not recipe:
        return jsonify({'error': 'Unknown recipe.'}), 400

    # Verify ingredients
    ingredients = recipe['ingredients']
    has_ingredients = all(state['inventory'].count(item) >= ingredients.count(item) for item in set(ingredients))
    
    if not has_ingredients:
        return jsonify({'error': 'Missing raw materials.'}), 400

    # Remove ingredients, add result
    for item in ingredients:
        state['inventory'].remove(item)
    state['inventory'].append(result_item)

    save_json(STATE_FILE, state)
    return jsonify({'state': state, 'message': f'Successfully crafted {result_item.replace("_", " ").title()}!'})

@app.route('/api/safehouse', methods=['POST'])
def safehouse_action():
    req = request.json
    action = req.get('action', '')

    state = load_json(STATE_FILE)

    if action == 'sleep':
        # Sleeping restores temporal sync
        restore_val = 30 * state['safehouse_upgrades']['bed_level']
        state['stats']['temporal_sync'] = min(100, state['stats']['temporal_sync'] + restore_val)
        state['stats']['notoriety'] = max(0, state['stats']['notoriety'] - 10)
        message = "You rested in the pod. Temporal alignment restored."

    elif action == 'eat':
        # Eating restores vitality, costs currency depending on current era
        cost = 20
        if state['wallet']['florins'] >= cost:
            state['wallet']['florins'] -= cost
            state['stats']['vitality'] = min(100, state['stats']['vitality'] + 25)
            message = "Consumed historical dish. Physical Vitality restored."
        else:
            return jsonify({'error': 'Insufficient Florins to purchase rations.'}), 400
            
    elif action == 'upgrade_bed':
        cost = 150
        if state['wallet']['florins'] >= cost:
            state['wallet']['florins'] -= cost
            state['safehouse_upgrades']['bed_level'] += 1
            message = "Upgraded sleeping quarters. Rest efficiency increased!"
        else:
            return jsonify({'error': 'Insufficient Florins for upgrades.'}), 400
    else:
        return jsonify({'error': 'Invalid action.'}), 400

    save_json(STATE_FILE, state)
    return jsonify({'state': state, 'message': message})

@app.route('/api/sidegig', methods=['POST'])
def sidegig():
    req = request.json
    answer = int(req.get('answer', 0))
    expected = int(req.get('expected', 0))
    reward = int(req.get('reward', 25))

    if answer != expected:
        return jsonify({'error': 'Ledger balance check failed. Math error detected!'}), 400

    state = load_json(STATE_FILE)
    state['wallet']['florins'] += reward
    save_json(STATE_FILE, state)

    return jsonify({'state': state, 'message': f'Verification successful! Credited {reward} Florins.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5080, debug=True)
