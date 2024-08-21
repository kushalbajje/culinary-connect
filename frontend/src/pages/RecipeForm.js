import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, TextField, Button, Typography, MenuItem } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { createRecipe, updateRecipe, getRecipe } from '../services/api';

const useStyles = makeStyles((theme) => ({
  container: {
    marginTop: theme.spacing(4),
    marginBottom: theme.spacing(4),
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: theme.spacing(2),
  },
  submit: {
    marginTop: theme.spacing(2),
  },
}));

const RecipeForm = () => {
  const classes = useStyles();
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    ingredients: '',
    instructions: '',
    preparation_time: '',
    cooking_time: '',
    servings: '',
    difficulty: '',
    category: '',
    cuisine: '',
  });

  useEffect(() => {
    if (id) {
      const fetchRecipe = async () => {
        try {
          const data = await getRecipe(id);
          setFormData(data);
        } catch (error) {
          console.error('Failed to fetch recipe:', error);
        }
      };
      fetchRecipe();
    }
  }, [id]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (id) {
        await updateRecipe(id, formData);
      } else {
        await createRecipe(formData);
      }
      navigate('/');
    } catch (error) {
      console.error('Failed to save recipe:', error);
    }
  };

  return (
    <Container className={classes.container}>
      <Typography variant="h4" component="h1" gutterBottom>
        {id ? 'Edit Recipe' : 'Create New Recipe'}
      </Typography>
      <form onSubmit={handleSubmit} className={classes.form}>
        <TextField
          name="title"
          label="Title"
          value={formData.title}
          onChange={handleChange}
          required
        />
        <TextField
          name="description"
          label="Description"
          value={formData.description}
          onChange={handleChange}
          multiline
          rows={3}
        />
        <TextField
          name="ingredients"
          label="Ingredients (comma-separated)"
          value={formData.ingredients}
          onChange={handleChange}
          multiline
          rows={5}
          required
        />
        <TextField
          name="instructions"
          label="Instructions"
          value={formData.instructions}
          onChange={handleChange}
          multiline
          rows={5}
          required
        />
        <TextField
          name="preparation_time"
          label="Preparation Time (minutes)"
          type="number"
          value={formData.preparation_time}
          onChange={handleChange}
          required
        />
        <TextField
          name="cooking_time"
          label="Cooking Time (minutes)"
          type="number"
          value={formData.cooking_time}
          onChange={handleChange}
          required
        />
        <TextField
          name="servings"
          label="Servings"
          type="number"
          value={formData.servings}
          onChange={handleChange}
          required
        />
        <TextField
          name="difficulty"
          label="Difficulty"
          select
          value={formData.difficulty}
          onChange={handleChange}
          required
        >
          <MenuItem value="easy">Easy</MenuItem>
          <MenuItem value="medium">Medium</MenuItem>
          <MenuItem value="hard">Hard</MenuItem>
        </TextField>
        <TextField
          name="category"
          label="Category"
          value={formData.category}
          onChange={handleChange}
          required
        />
        <TextField
          name="cuisine"
          label="Cuisine"
          value={formData.cuisine}
          onChange={handleChange}
          required
        />
        <Button type="submit" variant="contained" color="primary" className={classes.submit}>
          {id ? 'Update Recipe' : 'Create Recipe'}
        </Button>
      </form>
    </Container>
  );
};

export default RecipeForm;