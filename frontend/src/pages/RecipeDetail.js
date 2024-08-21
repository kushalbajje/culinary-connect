import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Typography, Button, List, ListItem, ListItemText, Divider } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { getRecipe, deleteRecipe } from '../services/api';

const useStyles = makeStyles((theme) => ({
  container: {
    marginTop: theme.spacing(4),
    marginBottom: theme.spacing(4),
  },
  title: {
    marginBottom: theme.spacing(2),
  },
  section: {
    marginTop: theme.spacing(3),
    marginBottom: theme.spacing(3),
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

  useEffect(() => {
    const fetchRecipe = async () => {
      try {
        const data = await getRecipe(id);
        setRecipe(data);
      } catch (error) {
        console.error('Failed to fetch recipe:', error);
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
      navigate('/');
    } catch (error) {
      console.error('Failed to delete recipe:', error);
    }
  };

  if (!recipe) {
    return <Typography>Loading...</Typography>;
  }

  // Split the ingredients string into an array
  const ingredientsList = recipe.ingredients.split(',').map(item => item.trim());

  return (
    <Container className={classes.container}>
      <Typography variant="h4" component="h1" className={classes.title}>
        {recipe.title}
      </Typography>
      <Typography variant="body1">{recipe.description}</Typography>
      <div className={classes.section}>
        <Typography variant="h6">Ingredients:</Typography>
        <List>
          {ingredientsList.map((ingredient, index) => (
            <ListItem key={index}>
              <ListItemText primary={ingredient} />
            </ListItem>
          ))}
        </List>
      </div>
      <Divider />
      <div className={classes.section}>
        <Typography variant="h6">Instructions:</Typography>
        <Typography variant="body1">{recipe.instructions}</Typography>
      </div>
      <Divider />
      <div className={classes.section}>
        <Typography>Preparation Time: {recipe.preparation_time} minutes</Typography>
        <Typography>Cooking Time: {recipe.cooking_time} minutes</Typography>
        <Typography>Servings: {recipe.servings}</Typography>
        <Typography>Difficulty: {recipe.difficulty}</Typography>
        <Typography>Category: {recipe.category}</Typography>
        <Typography>Cuisine: {recipe.cuisine}</Typography>
      </div>
      <Button variant="contained" color="primary" onClick={handleEdit} className={classes.button}>
        Edit Recipe
      </Button>
      <Button variant="contained" color="secondary" onClick={handleDelete}>
        Delete Recipe
      </Button>
    </Container>
  );
};

export default RecipeDetail;