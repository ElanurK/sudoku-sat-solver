# Sudoku SAT Solver & OCR ✨

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-pink)
![PySAT](https://img.shields.io/badge/Solver-PySAT-orange)
![Gemini API](https://img.shields.io/badge/AI-Gemini%20API-brightgreen)

This project is an image-processing-supported desktop application that checks if a Sudoku puzzle is solvable. It does this by encoding the puzzle into a Boolean Satisfiability (SAT) problem using Propositional Logic to find all valid solutions. I originally developed this as an academic project for the Software Engineering Department at Karadeniz Technical University (KTU).

## 🌟 Features

* **AI-Powered OCR:** The app uses the Google Gemini 2.5 Flash model to analyze uploaded Sudoku images and converts them into 9x9 digital grids.
* **SAT Encoding (Boolean Satisfiability):** It translates standard Sudoku rules (row, column, and block constraints) into Conjunctive Normal Form (CNF) to build a logical model.
* **Advanced Solving:** I used the `python-sat` library and the industry-standard `glucose3` solver to calculate all possible solutions for a puzzle (up to 100 solutions).
* **Asynchronous Architecture:** Heavy solving tasks and API wait times run in the background thanks to threading and queue mechanisms. This means the graphical user interface (GUI) never freezes, giving you a smooth experience.
* **Modern & Aesthetic GUI:** The app features a custom pink color palette, animated status notifications, and a handy "Solution Explorer" to easily navigate through the found solutions.

## ⚙️ System Architecture

1. **Input:** You can either upload a picture of a Sudoku puzzle or type the numbers manually.
2. **OCR Handler:** The image is sent to the Gemini API in Base64 format. The API then returns a 9x9 grid in JSON format.
3. **SAT Encoder:** The system converts the grid into a CNF formula using 729 boolean variables based on Sudoku's mathematical rules.
4. **SAT Solver:** The formula is solved. Once a solution is found, a *blocking clause* is added to the solver so it can continue searching for other valid solutions.

---
*Code with pink ≽^•⩊•^≼ ₊˚⊹♡*
