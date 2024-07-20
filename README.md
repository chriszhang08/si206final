# Project Title

## 1. Goals for Your Project (10 points)

- **Goal 1:** Do a basic spanish language analysis of vowel frequency in 2 completely different texts.
- **Goal 2:** Demonstrate a holistic understanding of the SI 206 curriculum by completing a project that integrates the
  skills learned in the course.

## 2. Goals that Were Achieved (10 points)

- **Achieved Goal 1:** Discovered that the letter "a" is the most common vowel in both texts, as is the letter "e".
- **Achieved Goal 2:** [Description of the second achieved goal]

## 3. Problems that You Faced (10 points)

- **Problem 1:** The hardest part about the project was probably figuring out how to limit the results from the API
  response, since the endpoint wasn't paginated.

## 5. Visualization that You Created (10 points)

![Visualization](path/to/visualization.png)
[Provide a description of the visualization]

## 6. Instructions for Running Your Code (10 points)


### Prerequisites

Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Setting Up the Environment

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/chriszhang08/si206final.git
   cd your-repository
   ```

2. **Set up your IDE:**

   This really depends on your IDE of choice, but happy to help out during office hours :)


3. **Install Dependencies:**

   Use `pip` to install the required packages from `requirements.txt`:

   ```sh
   pip install -r requirements.txt
   ```


## 7. Documentation for Each Function (20 points)

### Function: `pokedex_query`

- **Input:** a list of Pokemon unique ids
- **Output:** the Spanish flavor text of each Pokemon

This function queries the local SQLite database for the existing API endpoint associated with each Pokemon.
The function then searches for the Spanish flavor text of each Pokemon in the input list, and inserts it to the database.

## 8. Resources Used (20 points)

- **Resource 1:** [PokeAPI](https://pokeapi.co/)
- **Resource 3:** [BeautifulSoup Source Article (Copa 2024 Final)](https://www.bbc.com/mundo/articles/c0w4q32wzvpo)