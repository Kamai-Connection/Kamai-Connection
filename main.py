import tkinter as tk
from tkinter import messagebox

class Worker:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills

class Businessman:
    def __init__(self, name, contact, work_needed):
        self.name = name
        self.contact = contact
        self.work_needed = work_needed

class LinkInApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KK App")

        self.businessmen = []
        self.workers = []

        self.bg_image = tk.PhotoImage(file="C:/Users/User/Downloads/SIGN UP PAGE.png")

        self.load_data()  # Load data from files

        self.create_widgets()

    def create_widgets(self):
        self.root.configure(bg='light blue') 
        tk.Label(self.root, text="Welcome to Kamai Konnect", font=("Helvetica", 16), bg='white').pack(pady=10)

        tk.Button(self.root, text="Register Worker", command=self.register_worker).pack()
        tk.Button(self.root, text="Register Businessman", command=self.register_businessman).pack()
        tk.Button(self.root, text="Display All Workers", command=self.display_workers_list).pack()
        tk.Button(self.root, text="Display All Businessmen", command=self.display_businessmen_list).pack()
        tk.Button(self.root, text="Find Suitable Job Offers", command=self.find_suitable_jobs).pack()
        tk.Button(self.root, text="Display Worker Ratings", command=self.display_worker_ratings).pack()

    def create_background_frame(self, window):
        bg_frame = tk.Frame(window)
        bg_frame.pack(fill=tk.BOTH, expand=True)

        bg_label = tk.Label(bg_frame, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        return bg_frame

    def load_data(self):
        try:
            with open("workers.txt", "r") as file:
                for line in file:
                    name, skills = line.strip().split(',')
                    self.workers.append(Worker(name, skills.split(',')))
        except FileNotFoundError:
            pass

        try:
            with open("businessmen.txt", "r") as file:
                for line in file:
                    name, contact, work_needed = line.strip().split(',')
                    self.businessmen.append(Businessman(name, contact, work_needed))
        except FileNotFoundError:
            pass

    def save_data(self):
        with open("workers.txt", "w") as file:
            for worker in self.workers:
                file.write(f"{worker.name},{','.join(worker.skills)}\n")

        with open("businessmen.txt", "w") as file:
            for businessman in self.businessmen:
                file.write(f"{businessman.name},{businessman.contact},{businessman.work_needed}\n")

    def register_worker(self):
        worker_window = tk.Toplevel(self.root)
        worker_window.title("Register Worker")
        bg_frame = self.create_background_frame(worker_window)

        tk.Label(bg_frame, text="Enter the name of the worker:").pack()
        worker_name_entry = tk.Entry(bg_frame)
        worker_name_entry.pack()

        tk.Label(bg_frame, text="Enter the skills of the worker (separated by comma):").pack()
        worker_skills_entry = tk.Entry(bg_frame)
        worker_skills_entry.pack()

        def save_worker():
            name = worker_name_entry.get()
            skills = worker_skills_entry.get().split(',')
            worker = Worker(name, skills)
            self.workers.append(worker)
            messagebox.showinfo("Success", "Worker details saved successfully!")
            worker_window.destroy()
            self.save_data()  # Save data to files

        tk.Button(bg_frame, text="Save Worker", command=save_worker).pack()

    def register_businessman(self):
        businessman_window = tk.Toplevel(self.root)
        businessman_window.title("Register Businessman")
        bg_frame = self.create_background_frame(businessman_window)

        tk.Label(bg_frame, text="Enter the name of the businessman:").pack()
        businessman_name_entry = tk.Entry(bg_frame)
        businessman_name_entry.pack()

        tk.Label(bg_frame, text="Enter the contact number:").pack()
        contact_entry = tk.Entry(bg_frame)
        contact_entry.pack()

        tk.Label(bg_frame, text="Enter the work needed:").pack()
        work_needed_entry = tk.Entry(bg_frame)
        work_needed_entry.pack()

        def save_businessman():
            name = businessman_name_entry.get()
            contact = contact_entry.get()
            work_needed = work_needed_entry.get()
            businessman = Businessman(name, contact, work_needed)
            self.businessmen.append(businessman)
            messagebox.showinfo("Success", "Businessman details saved successfully!")
            businessman_window.destroy()
            self.save_data()  # Save data to files

        tk.Button(bg_frame, text="Save Businessman", command=save_businessman).pack()

    def display_workers_list(self):
        workers_window = tk.Toplevel(self.root)
        workers_window.title("List of Workers")
        bg_frame = self.create_background_frame(workers_window)

        if not self.workers:
            tk.Label(bg_frame, text="No workers registered yet.").pack()
        else:
            for worker in self.workers:
                tk.Label(bg_frame, text=f"Name: {worker.name}, Skills: {', '.join(worker.skills)}").pack()

    def display_businessmen_list(self):
        businessmen_window = tk.Toplevel(self.root)
        businessmen_window.title("List of Businessmen")
        bg_frame = self.create_background_frame(businessmen_window)

        if not self.businessmen:
            tk.Label(bg_frame, text="No businessmen registered yet.").pack()
        else:
            for businessman in self.businessmen:
                tk.Label(bg_frame, text=f"Name: {businessman.name}, Contact: {businessman.contact}, Work Needed: {businessman.work_needed}").pack()

    def find_suitable_jobs(self):
        if not self.workers or not self.businessmen:
            messagebox.showwarning("Warning", "Please register workers and businessmen first.")
            return

        match_window = tk.Toplevel(self.root)
        match_window.title("Find Suitable Job Offers")
        bg_frame = self.create_background_frame(match_window)

        tk.Label(bg_frame, text="Select a worker:").pack()
        worker_var = tk.StringVar()
        worker_var.set("")  # Default value

        worker_options = [worker.name for worker in self.workers]
        tk.OptionMenu(bg_frame, worker_var, *worker_options).pack()

        def find_matches():
            selected_worker = next((worker for worker in self.workers if worker.name == worker_var.get()), None)
            if selected_worker is None:
                messagebox.showerror("Error", "Selected worker not found.")
                return

            matching_businessmen = []
            for businessman in self.businessmen:
                needed_skills = set(businessman.work_needed.split(','))
                worker_skills = set(selected_worker.skills)
                if needed_skills.intersection(worker_skills):
                    matching_businessmen.append(businessman)

            if matching_businessmen:
                match_result = "\n".join([f"Name: {b.name}, Contact: {b.contact}, Work Needed: {b.work_needed}" for b in matching_businessmen])
                messagebox.showinfo("Match Result", f"Suitable businessmen for {selected_worker.name}:\n{match_result}")
            else:
                messagebox.showinfo("Match Result", f"No suitable businessmen found for {selected_worker.name}.")

        tk.Button(bg_frame, text="Find Matches", command=find_matches).pack()

    def display_worker_ratings(self):
        ratings_window = tk.Toplevel(self.root)
        ratings_window.title("Worker Ratings")
        bg_frame = self.create_background_frame(ratings_window)

        ratings = [
            "anshika  5*",
            "sneha    4*",
            "kashish  4*"
        ]

        for rating in ratings:
            tk.Label(bg_frame, text=rating).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkInApp(root)
    root.mainloop()

