import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Card, CardActionArea, CardContent, CardMedia, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
  root: {
    maxWidth: 345,
  },
  media: {
    height: 140,
  },
});

const RecipeCard = ({ recipe }) => {
  const classes = useStyles();

  return (
    <Card className={classes.root}>
      <CardActionArea component={RouterLink} to={`/recipe/${recipe.id}`}>
        <CardMedia
          className={classes.media}
          image={recipe.image || 'https://via.placeholder.com/345x140.png?text=No+Image'}
          title={recipe.title}
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="h2">
            {recipe.title}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            {recipe.description}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            Difficulty: {recipe.difficulty}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            Preparation Time: {recipe.preparation_time} minutes
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};

export default RecipeCard;