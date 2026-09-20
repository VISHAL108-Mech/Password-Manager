# 🔐 Password Manager

A desktop **Password Manager** built with Python's `tkinter` GUI toolkit — generate strong random passwords, save them per website, and look them up later, all stored locally in a JSON file with a clean dark-themed interface.

> Enter a website, hit "Generate Password," and save it. Come back later and search by website name to retrieve your saved credentials instantly.

---

## 🎮 Demo

<img width="400" height="300" alt="Screenshot 2026-09-20 155721" src="https://github.com/user-attachments/assets/39cb4d77-3de9-471c-b3cc-9fef110345b2" />
<img width="400" height="300" alt="Screenshot 2026-09-20 155847" src="https://github.com/user-attachments/assets/d3441ca9-70bf-4665-b397-7de39098bd25" />
<img width="400" height="300" alt="Screenshot 2026-09-20 160847" src="https://github.com/user-attachments/assets/40c2ea8a-05ae-4d88-babb-196ca75306fe" />
<img width="400" height="300" alt="Screenshot 2026-09-20 160100" src="https://github.com/user-attachments/assets/5716f02d-b0f6-44ec-aba5-ec21a0ef7804" />


---

## ✨ Features

- 🎲 **Secure random password generation** — mixes uppercase/lowercase letters, numbers, and symbols in randomized quantities and order.
- 📋 **One-click clipboard copy** — every generated password is automatically copied via `pyperclip`, so you can paste it straight into a signup form.
- 💾 **Persistent local storage** using a `data.json` file — no database setup required.
- 🔍 **Instant password lookup** by website name, displayed in a native popup dialog.
- 🛡️ **Input validation** — warns you if you try to save with empty fields instead of silently saving bad data.
- 🔄 **Non-destructive updates** — saving a new entry merges with existing saved data instead of overwriting the whole file.
- 🎨 **Custom dark-themed UI** with a consistent color palette and a lock icon graphic.

---

## 🛠️ Tech Stack

| Category | Tool / Concept |
|---|---|
| Language | Python 3 |
| GUI | `tkinter` (standard library) |
| Clipboard | `pyperclip` |
| Data Storage | `json` (standard library) — flat-file, no database |
| Randomization | `random` (`randint`, `choice`, `shuffle`) |
| Core Concepts | Event-driven GUI programming, file I/O, exception handling, data merging |

---

## 📂 Project Structure

```
Password Manager/
│
├── main.py          # Entry point — GUI layout, password generation, save/search logic
├── my_lock.png       # Lock icon displayed in the app window
├── data.json         # Auto-created on first save — stores website/email/password entries
└── README.md
```

`data.json` isn't included in the repo since it's generated automatically the first time you save an entry — this keeps your actual saved passwords out of version control.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x installed
- `tkinter` (ships with most Python installations)
- `pyperclip` — install via pip:

```bash
pip install pyperclip
```

### Run it
```bash
git clone https://github.com/VISHAL108-Mech/Password-Manager.git
cd password-manager
python main.py
```

### How to Use
| Action | Steps |
|---|---|
| **Generate a password** | Click "Generate Password" — a random password appears in the field and is copied to your clipboard |
| **Save an entry** | Fill in Website, Email/Username, and Password, then click "Add" |
| **Find a saved password** | Type a website name and click "Search" |

---

## 🧩 How It Works

### 1. Password Generation
Random passwords are built from three separate pools — letters, symbols, and numbers — each contributing a randomized count of characters, then shuffled together so the structure isn't predictable.

```python
def password_generator():
    """Generates a random password consisting of letters, numbers, and symbols."""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for letter in range(randint(8, 10))]
    password_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
    password_numbers = [choice(numbers) for number in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    input_password.insert(0, password)
    pyperclip.copy(password)
```

### 2. Saving Credentials
Before saving, the app checks that the required fields aren't empty. It then tries to read the existing `data.json` file — if it doesn't exist yet, a new one is created; if it does, the new entry is merged in with `.update()` so previous entries are never lost.

```python
def save():
    """Saves the website, email/username, and password to a JSON file."""
    website = input_website.get().lower()
    email_username = input_email_username.get()
    my_password = input_password.get()
    my_data = {
        website: {"email": email_username,
                  "password": my_password}
    }

    if len(website) == 0 or len(my_password) == 0:
        messagebox.askokcancel(title="Oops!",
                               message="Enter detail in empty fields!")

    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as f:
                json.dump(my_data, f, indent=4)
        else:
            data.update(my_data)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            input_website.delete(0, "end")
            input_password.delete(0, "end")
```

### 3. Finding a Saved Password
Looking up a website reads the JSON file, checks whether that website exists as a key, and displays the matching email/password pair in a popup — or a friendly message if nothing's found.

```python
def find_password():
    """Finds and displays the email and password for a given website."""
    find_website = input_website.get().lower()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error!", message="Data file not found.")
    else:
        if find_website not in data:
            messagebox.showinfo(title="Oops!",
                                message="No details found.")
        else:
            email = data[find_website]["email"]
            password = data[find_website]["password"]
            messagebox.showinfo(title=find_website,
                                message=f"Email: {email}\n"
                                        f"Password: {password}")
```

### 4. Building the Interface
The GUI is laid out with `tkinter`'s grid system — labels, entry fields, and buttons are positioned by row/column, with a custom dark color palette applied throughout for a polished look.

```python
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=background_darker)

canvas = Canvas(width=200, height=200, bg=background_darker,
                highlightthickness=0)
lock_image = PhotoImage(file="my_lock.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(row=1, column=2)
```

---

## 📚 What This Project Demonstrates

- Building a functional desktop GUI application with `tkinter`'s widget and grid layout system
- Generating cryptographically-varied (though not cryptographically secure) passwords using multiple character pools
- Persisting structured data locally with `json`, including safe read/write/merge patterns
- Handling real-world edge cases: missing files (`FileNotFoundError`), empty form fields, and non-existent lookups
- Integrating third-party libraries (`pyperclip`) to extend built-in functionality
- Designing a cohesive UI color scheme using named, reusable variables instead of scattered hex codes

---

## 🔮 Future Improvements

- [ ] Add master-password protection / encryption for `data.json` (plaintext storage isn't secure)
- [ ] Add a "Show Password" toggle instead of relying on clipboard/popup only
- [ ] Add the ability to edit or delete existing saved entries
- [ ] Add password strength indication when generating
- [ ] Migrate storage to an encrypted local database (e.g. SQLite with encryption)

---

## 👤 Developer

**VISHAL YADAV**
- GitHub: [@VISHAL108-Mech](https://github.com/VISHAL108-Mech)
- LinkedIn: [vishal-yadav-2a91a7428](https://www.linkedin.com/in/vishal-yadav-2a91a7428)
- Email: [vy4122000@gmail.com](mailto:vy4122000@gmail.com)
