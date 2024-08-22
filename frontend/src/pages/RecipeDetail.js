import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Container,
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
  Paper,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import { getRecipe, deleteRecipe } from "../services/api";
import useAuth from "../hooks/useAuth"; // Import the useAuth hook
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const useStyles = makeStyles((theme) => ({
  container: {
    marginTop: theme.spacing(4),
    marginBottom: theme.spacing(4),
  },
  goBackButton: {
    marginBottom: theme.spacing(2),
  },
  title: {
    marginBottom: theme.spacing(2),
    fontWeight: "bold",
    textAlign: "center",
  },
  imageContainer: {
    position: "relative",
    overflow: "hidden",
    height: "400px",
    marginBottom: theme.spacing(3),
    borderRadius: "8px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  },
  image: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
  },
  contentContainer: {
    paddingTop: "10px",
  },
  section: {
    marginTop: theme.spacing(3),
    marginBottom: theme.spacing(3),
    padding: theme.spacing(3),
    backgroundColor: "#f9f9f9",
    borderRadius: "8px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  },
  sectionTitle: {
    marginBottom: theme.spacing(1),
    fontWeight: "bold",
    color: theme.palette.primary.main,
  },
  ingredientItem: {
    display: "flex",
    alignItems: "center",
    padding: theme.spacing(1),
    borderBottom: "1px solid #ddd",
    "&:last-child": {
      borderBottom: "none",
    },
  },
  buttonContainer: {
    marginTop: theme.spacing(3),
    textAlign: "center",
  },
  button: {
    marginRight: theme.spacing(2),
  },
}));

const RecipeDetail = () => {
  const classes = useStyles();
  const { id } = useParams();
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState(null);
  const { user } = useAuth(); // Get the current user's information

  useEffect(() => {
    const fetchRecipe = async () => {
      try {
        const data = await getRecipe(id);
        setRecipe(data);
      } catch (error) {
        console.error("Failed to fetch recipe:", error);
      }
    };

    fetchRecipe();
  }, [id]);

  const handleEdit = () => {
    navigate(`/edit-recipe/${id}`);
  };

  const handleDelete = async () => {
    try {
      await deleteRecipe(id);
      toast.success("Recipe deleted successfully!");
      setTimeout(() => {
        navigate("/profile");
      }, 2000);  // Delay navigation to allow the toast to be seen
    } catch (error) {
      console.error("Failed to delete recipe:", error);
      toast.error("Failed to delete recipe. Please try again.");
    }
  };
  

  const handleGoBack = () => {
    navigate(-1); // Go back to the previous page
  };

  if (!recipe) {
    return <Typography>Loading...</Typography>;
  }

  // Split the ingredients string into an array
  const ingredientsList = recipe.ingredients
    .split(",")
    .map((item) => item.trim());

  return (
    <Container className={classes.container}>
      <Button
        variant="contained"
        color="default"
        onClick={handleGoBack}
        className={classes.goBackButton}
      >
        Go Back
      </Button>
      <Typography variant="h4" component="h1" className={classes.title}>
        {recipe.title}
      </Typography>
      {/* Display Recipe Image */}
      {recipe.image_url && (
        <div className={classes.imageContainer}>
          <img
            src={recipe.image_url}
            alt={recipe.title}
            className={classes.image}
          />
        </div>
      )}
      <div className={classes.contentContainer}>
        <Paper className={classes.section} elevation={3}>
          <Typography variant="h6" className={classes.sectionTitle}>
            Description:
          </Typography>
          <Typography variant="body1">{recipe.description}</Typography>
        </Paper>
        <Paper className={classes.section} elevation={3}>
          <Typography variant="h6" className={classes.sectionTitle}>
            Ingredients:
          </Typography>
          <List>
            {ingredientsList.map((ingredient, index) => (
              <ListItem key={index} className={classes.ingredientItem}>
                <ListItemText primary={ingredient} />
              </ListItem>
            ))}
          </List>
        </Paper>
        <Paper className={classes.section} elevation={3}>
          <Typography variant="h6" className={classes.sectionTitle}>
            Instructions:
          </Typography>
          <Typography variant="body1">{recipe.instructions}</Typography>
        </Paper>
        <Paper className={classes.section} elevation={3}>
          <Typography variant="h6" className={classes.sectionTitle}>
            Additional Information:
          </Typography>
          <Typography>
            Preparation Time: {recipe.preparation_time} minutes
          </Typography>
          <Typography>Cooking Time: {recipe.cooking_time} minutes</Typography>
          <Typography>Servings: {recipe.servings}</Typography>
          <Typography>Difficulty: {recipe.difficulty}</Typography>
          <Typography>Category: {recipe.category}</Typography>
          <Typography>Cuisine: {recipe.cuisine}</Typography>
        </Paper>
        <div className={classes.buttonContainer}>
          {user && user.username === recipe.author && (
            <>
              <Button
                variant="contained"
                color="primary"
                onClick={handleEdit}
                className={classes.button}
              >
                Edit Recipe
              </Button>
              <Button
                variant="contained"
                color="secondary"
                onClick={handleDelete}
              >
                Delete Recipe
              </Button>
            </>
          )}
        </div>
      </div>
      <ToastContainer />
    </Container>
  );
};

export default RecipeDetail;
