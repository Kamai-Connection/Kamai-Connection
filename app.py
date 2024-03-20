from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Placeholder data (replace with database integration)
workers = []
businessmen = []

def load_data():
    global workers, businessmen
    try:
        with open('workers.txt', 'r') as file:
            for line in file:
                name, skills = line.strip().split(',')
                workers.append({'name': name, 'skills': skills.split(',')})
    except FileNotFoundError:
        pass

    try:
        with open('businessmen.txt', 'r') as file:
            for line in file:
                name, contact, work_needed = line.strip().split(',')
                businessmen.append({'name': name, 'contact': contact, 'work_needed': work_needed})
    except FileNotFoundError:
        pass

# Load data from files on server startup
load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_worker')
def register_worker():
    return render_template('register_worker.html')

@app.route('/register_businessman')
def register_businessman():
    return render_template('register_businessman.html')

@app.route('/display_workers')
def display_workers():
    return render_template('workers_list.html', workers=workers)

@app.route('/display_businessmen')
def display_businessmen():
    return render_template('business_list.html', businessmen=businessmen)

@app.route('/save_worker', methods=['POST'])
def save_worker():
    name = request.form['workerName']
    skills = request.form['workerSkills'].split(',')
    worker = {'name': name, 'skills': skills}
    workers.append(worker)

    # Save worker data to a text file
    with open('workers.txt', 'a') as file:
        file.write(f"{worker['name']},{','.join(worker['skills'])}\n")

    return jsonify({'message': 'Worker registered successfully!'})

@app.route('/save_businessman', methods=['POST'])
def save_businessman():
    name = request.form['businessmanName']
    contact = request.form['contactNumber']
    work_needed = request.form['workNeeded']
    businessman = {'name': name, 'contact': contact, 'work_needed': work_needed}
    businessmen.append(businessman)

    # Save businessman data to a text file
    with open('businessmen.txt', 'a') as file:
        file.write(f"{businessman['name']},{businessman['contact']},{businessman['work_needed']}\n")

    return jsonify({'message': 'Businessman registered successfully!'})

@app.route('/find_job_offers', methods=['GET', 'POST'])
def find_job_offers():
    if request.method == 'POST':
        selected_worker = request.form['selectedWorker']
        matching_businessmen = []
        for worker in workers:
            if worker['name'] == selected_worker:
                worker_skills = set(worker['skills'])
                for businessman in businessmen:
                    needed_skills = set(businessman['work_needed'].split(','))
                    if needed_skills.issubset(worker_skills):
                        matching_businessmen.append(businessman)
        return render_template('find_job_offers.html', matching_businessmen=matching_businessmen)
    else:
        # Handle GET request (if needed)
        return render_template('find_job_offers.html', matching_businessmen=[])

if __name__ == '__main__':
    app.run(debug=True)