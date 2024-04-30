// Sample data (replace with actual data fetched from the server)
const dishDetails = {
    preparationTime: '30 minutes',
    cuisineType: 'Indian',
    ingredients: ['Ingredient 1', 'Ingredient 2', 'Ingredient 3'],
    directions: ['Step 1', 'Step 2', 'Step 3'],
  };
  
  const comments = [
    { text: 'Comment 1', date: '2024-04-30' },
    { text: 'Comment 2', date: '2024-04-29' },
    { text: 'Comment 3', date: '2024-04-28' },
  ];
  
  // Function to populate dish details
  function populateDishDetails() {
    document.getElementById('prep-time').innerText = dishDetails.preparationTime;
    document.getElementById('cuisine-type').innerText = dishDetails.cuisineType;
  
    const ingredientsList = document.getElementById('ingredients-list');
    dishDetails.ingredients.forEach(ingredient => {
      const li = document.createElement('li');
      li.textContent = ingredient;
      ingredientsList.appendChild(li);
    });
  
    const directionsList = document.getElementById('directions-list');
    dishDetails.directions.forEach(direction => {
      const li = document.createElement('li');
      li.textContent = direction;
      directionsList.appendChild(li);
    });
  }
  
  // Function to populate comments
  function populateComments() {
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = '';
    comments.forEach(comment => {
      const div = document.createElement('div');
      div.classList.add('comment');
      div.innerHTML = `
        <p>${comment.text}</p>
        <p class="comment-date">${comment.date}</p>
      `;
      commentsList.appendChild(div);
    });
  }
  
  // Function to post a new comment
  function postComment() {
    const commentText