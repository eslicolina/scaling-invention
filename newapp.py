import streamlit as st
import pandas as pd
import pickle
import os # Import the os module

# --- Cargar los archivos guardados ---
# Define the file paths
movie_list_path = 'movie_list.pkl'
similarity_path = 'similarity.pkl'

# Check if files exist before loading
if not os.path.exists(movie_list_path) or not os.path.exists(similarity_path):
    st.error("Archivos 'movie_list.pkl' o 'similarity.pkl' no encontrados.")
    st.warning("Por favor, ejecuta las celdas anteriores en Colab para generar estos archivos.")
    st.stop() # Stop the Streamlit app if files are missing

try:
    # Load the movies DataFrame
    with open(movie_list_path, 'rb') as f:
        movies = pickle.load(f)

    # Load the cosine similarity matrix
    with open(similarity_path, 'rb') as f:
        cosine_sim = pickle.load(f)


except Exception as e:
    st.error(f"Error al cargar los archivos: {e}")
    st.stop()

# Create a Series mapping movie titles to indices (this needs to be recreated)
# Ensure the 'title' column exists in the loaded movies DataFrame
if 'title' in movies.columns:
    indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()
   
else:
    st.error("La columna 'title' no se encontró en el DataFrame cargado.")
    st.stop()


# --- Definir la función de recomendación ---
# Define the recommendation function
def get_recommendations(title, cosine_sim=cosine_sim, movies=movies, indices=indices):
    # Get the index of the movie that matches the title
    if title not in indices.index:
        return f"Película '{title}' no encontrada."
    idx = indices[title]

    # Get the pairwise similarity scores for all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies (excluding the movie itself)
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return movies['title'].iloc[movie_indices]

# --- Crear la interfaz web con Streamlit ---
st.title('Recomendación de Películas')

movie_title = st.text_input('Ingresa el título de una película:')

if st.button('Obtener Recomendaciones'):
    if movie_title:
        recommendations = get_recommendations(movie_title)
        if isinstance(recommendations, str):
            st.warning(recommendations) # Display message if movie not found
        else:
            st.subheader(f"Recomendaciones para '{movie_title}':")
            for rec in recommendations:
                st.write(f"- {rec}")

        # --- Sección para agregar una reseña ---
        st.markdown("---")
        st.subheader(f"Agrega tu reseña para '{movie_title}':")
        user_review = st.text_area("Escribe tu reseña aquí:")

        if st.button("Enviar Reseña"):
            if user_review:
                # Aquí puedes procesar la reseña (por ejemplo, guardarla en un archivo, base de datos, etc.)
                # Por ahora, simplemente mostraremos la reseña enviada.
                st.write("¡Gracias por tu reseña!")
                st.write(f"Tu reseña para '{movie_title}':")
                st.write(user_review)
            else:
                st.warning("Por favor, escribe algo en la reseña antes de enviarla.")

    else:
        st.info('Por favor, ingresa el título de una película.')

st.markdown("---")
st.write("Hola Mundo.")

# --- Agregar información del autor ---
st.markdown("---")
st.write("Creado por: [EsliAsareel]") # Reemplaza "[Tu Nombre Aquí]" con tu nombre
