from flask import Flask, render_template, request, session
from database import init_db, populate_db, get_random_cocktail

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session management

@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize score and guess count in session if they don't exist
    if "score" not in session:
        session["score"] = 0
    if "guess_count" not in session:
        session["guess_count"] = 0

    if request.method == "POST":
        user_guess = request.form.get("guess").lower()
        correct_name = request.form.get("correct_name").lower()
        image_url = request.form.get("image_url")
        current_progress = list(request.form.get("current_progress"))
        guess_count = int(request.form.get("guess_count")) + 1

        # Update progress with correct guesses for multiple letters
        for index, letter in enumerate(correct_name):
            if letter in user_guess:
                current_progress[index] = letter

        # Check if the user has completed the word
        if "_" not in current_progress:
            session["score"] += 1
            result = f"Congratulations! You guessed the cocktail: {correct_name.title()}!"
            return render_template(
                "index.html",
                result=result,
                score=session["score"],
                next_round=True,
                image_url=image_url,
                current_progress=current_progress,
                guess_count=guess_count,
            )

        # Continue guessing
        return render_template(
            "index.html",
            current_progress=current_progress,
            cocktail_name=correct_name,
            image_url=image_url,
            score=session["score"],
            guess_count=guess_count,
        )

    # Generate a random cocktail for the new round (GET request or after clicking "Guess More")
    cocktail_name, ingredients, image_url = get_random_cocktail()
    # Clean up cocktail name and ensure proper capitalization
    cocktail_name = ' '.join(word.capitalize() for word in cocktail_name.split())
    current_progress = ["_" if c.isalpha() else c for c in cocktail_name.lower()]
    session["guess_count"] = 0

    return render_template(
        "index.html",
        ingredients=ingredients,
        cocktail_name=cocktail_name,
        image_url=image_url,
        current_progress=current_progress,
        score=session["score"],
        guess_count=session["guess_count"],
    )

if __name__ == "__main__":
    print("Setting up the database...")
    init_db()
    populate_db()
    print("Database is ready. Running Cocktail Guessing Game...")
    app.run(debug=True)
