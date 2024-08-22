import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, TextField, Button, Typography, MenuItem } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { createRecipe, updateRecipe, getRecipe } from '../services/api';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

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
  buttonContainer: {
    display: 'flex',
    justifyContent: 'space-between',
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
    image: null,
  });
  const [formIsValid, setFormIsValid] = useState(false);

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

  useEffect(() => {
    const checkFormValidity = () => {
      const {
        title, description, ingredients, instructions, preparation_time,
        cooking_time, servings, difficulty, category, cuisine, image
      } = formData;

      const isValid = title && ingredients && instructions && preparation_time && description &&
                      cooking_time && servings && difficulty && category && cuisine && image;
      setFormIsValid(isValid);
    };

    checkFormValidity();
  }, [formData]);

  const handleChange = (e) => {
    if (e.target.name === 'image') {
      setFormData({ ...formData, image: e.target.files[0] });
    } else {
      setFormData({ ...formData, [e.target.name]: e.target.value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const recipeData = new FormData();
    for (const key in formData) {
      recipeData.append(key, formData[key]);
    }

    try {
      if (id) {
        await updateRecipe(id, recipeData);
        toast.success('Recipe updated successfully!');
      } else {
        await createRecipe(recipeData);
        toast.success('Recipe created successfully!');
      }
      setTimeout(() => {
        navigate('/');
      }, 2000);  // Redirect after a short delay to allow the toast to be seen
    } catch (error) {
      console.error('Failed to save recipe:', error);
      toast.error('Failed to save recipe!');
    }
  };

  const handleCancel = () => {
    navigate(-1);  // Go back to the previous page
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
          rows={2}
          required
        />
        <TextField
          name="ingredients"
          label="Ingredients (comma-separated)"
          value={formData.ingredients}
          onChange={handleChange}
          multiline
          rows={2}
          required
        />
        <TextField
          name="instructions"
          label="Instructions"
          value={formData.instructions}
          onChange={handleChange}
          multiline
          rows={3}
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
        <input
          accept="image/*"
          style={{ display: 'none' }}
          id="raised-button-file"
          type="file"
          name="image"
          onChange={handleChange}
        />
        <label htmlFor="raised-button-file">
          <Button variant="contained" color="primary" component="span">
            Upload Image
          </Button>
          {formData.image && <Typography>{formData.image.name}</Typography>}
        </label>
        <div className={classes.buttonContainer}>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            className={classes.submit}
            disabled={!formIsValid}
          >
            {id ? 'Update Recipe' : 'Create Recipe'}
          </Button>
          {id && (
            <Button
              variant="contained"
              color="default"
              onClick={handleCancel}
              className={classes.submit}
            >
              Cancel
            </Button>
          )}
        </div>
      </form>
      <ToastContainer />
    </Container>
  );
};

export default RecipeForm;
