
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk
import ast  # Import ast module for safer literal evaluation
from PIL import Image, ImageTk
import tkinter as tk


# Load the predefined ramen recipes data
recipes_df = pd.read_csv('ramen_recipes.csv')

# Function to recommend recipes based on user preferences
def recommend_recipes(user_preferences):
    # Convert user preferences to a DataFrame
    user_df = pd.DataFrame([user_preferences], columns=['spiciness', 'richness', 'sweetness', 'umami'])

    # Calculate cosine similarity between user preferences and recipe attributes
    similarity_scores = cosine_similarity(user_df, recipes_df[['spiciness', 'richness', 'sweetness', 'umami']])

    # Get indices of top recommended recipes based on similarity scores
    top_recipe_indices = np.argsort(similarity_scores[0])[::-1][:5]

    # Extract and return the recommended recipes and ingredients
    recommended_recipes = recipes_df.iloc[top_recipe_indices][['recipe_name', 'spiciness', 'richness', 'sweetness', 'umami', 'ingredients']]
    return recommended_recipes

# GUI Implementation
class RamenRecommenderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ramanova")
        self.master.configure(bg="#FFEBD7")

        image_path = "1.png"  # Replace with the path to your image file
        img = Image.open(image_path)
        resized_image = img.resize((200, 200))
        img = ImageTk.PhotoImage(resized_image)


        # Create a label to display the image at the top
        image_label = tk.Label(master, image=img)
        image_label.photo = img 

        # Create sliders for user preferences
        self.spiciness_label = ttk.Label(master, text="Spiciness:")
        self.spiciness_slider = ttk.Scale(master, from_=0, to=10, orient="horizontal")

        self.richness_label = ttk.Label(master, text="Richness:")
        self.richness_slider = ttk.Scale(master, from_=0, to=10, orient="horizontal")

        self.sweetness_label = ttk.Label(master, text="Sweetness:")
        self.sweetness_slider = ttk.Scale(master, from_=0, to=10, orient="horizontal")

        self.umami_label = ttk.Label(master, text="Umami:")
        self.umami_slider = ttk.Scale(master, from_=0, to=10, orient="horizontal")

        # Button to trigger recommendations
        self.recommend_button = ttk.Button(master, text="Get Recommendations", command=self.get_recommendations)

        # Textbox to display recommendations
        self.recommendations_text = tk.Text(master, height=15, width=150)

        # Place widgets on the grid
        image_label.grid(row=0, column=0, columnspan=2)
        self.spiciness_label.grid(row=1, column=0, pady=10)
        self.spiciness_slider.grid(row=1, column=1, pady=10)
        self.richness_label.grid(row=2, column=0, pady=10)
        self.richness_slider.grid(row=2, column=1, pady=10)
        self.sweetness_label.grid(row=3, column=0, pady=10)
        self.sweetness_slider.grid(row=3, column=1, pady=10)
        self.umami_label.grid(row=4, column=0, pady=10)
        self.umami_slider.grid(row=4, column=1, pady=10)
        self.recommend_button.grid(row=5, column=0, columnspan=2, pady=20)
        self.recommendations_text.grid(row=6, column=0, columnspan=2, pady=10)

        # Initialize a variable to store the previous recommendations
        self.previous_recommendations = None

    def get_recommendations(self):
        # Fetch user preferences from sliders
        spiciness = self.spiciness_slider.get()
        richness = self.richness_slider.get()
        sweetness = self.sweetness_slider.get()
        umami = self.umami_slider.get()

        # Get recommendations based on user preferences
        user_preferences = [spiciness, richness, sweetness, umami]
        recommended_recipes = recommend_recipes(user_preferences)

        # Display recommendations in the textbox
        self.recommendations_text.config(state=tk.NORMAL)
        self.recommendations_text.delete(1.0, tk.END)  # Clear previous recommendations

        # Check if the recommendations are the same as the previous ones
        if not self.are_recommendations_identical(recommended_recipes):
            self.recommendations_text.insert(tk.END, "Recommended Recipes:\n\n")
            for _, row in recommended_recipes.iterrows():
                ingredients_list = ast.literal_eval(row['ingredients'])  # Use ast.literal_eval for safer literal evaluation
                self.recommendations_text.insert(tk.END, f"{row['recipe_name']} - Ingredients: {', '.join(ingredients_list)}\n\n")
            self.previous_recommendations = recommended_recipes
        else:
            self.recommendations_text.insert(tk.END, "No new recommendations. Change sliders and try again.")

        self.recommendations_text.config(state=tk.DISABLED)

    def are_recommendations_identical(self, new_recommendations):
        # Check if the new recommendations are identical to the previous ones
        if self.previous_recommendations is None:
            return False
        return new_recommendations.equals(self.previous_recommendations)


   

def main():
    root = tk.Tk()
    app = RamenRecommenderApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()



