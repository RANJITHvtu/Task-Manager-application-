// app.js

// Function to open the update task modal
function openUpdateTaskModal(taskId) {
  // Fetch the task details from the server using AJAX
  fetch(`/get_task_details/${taskId}`)
      .then(response => response.json())
      .then(data => {
          // Assuming you have a modal with input fields for updating tasks
          document.getElementById('update-task-title').value = data.title;
          document.getElementById('update-task-description').value = data.description;

          // Show or toggle the visibility of the modal
          document.getElementById('updateTaskModal').style.display = 'block';
      })
      .catch(error => {
          console.error('Error fetching task details:', error);
      });
}

// Function to open the update category modal
function openUpdateCategoryModal(categoryId) {
  // Fetch the category details from the server using AJAX
  fetch(`/get_category_details/${categoryId}`)
      .then(response => response.json())
      .then(data => {
          // Assuming you have a modal with input fields for updating categories
          document.getElementById('update-category-name').value = data.name;

          // Show or toggle the visibility of the modal
          document.getElementById('updateCategoryModal').style.display = 'block';
      })
      .catch(error => {
          console.error('Error fetching category details:', error);
      });
}

// Function to update a task
function updateTask(taskId) {
  var title = document.getElementById('update-task-title').value;
  var description = document.getElementById('update-task-description').value;

  fetch(`/update_task/${taskId}`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
          'title': title,
          'description': description,
      }),
  })
  .then(response => response.json())
  .then(data => {
      console.log(data.message);
      // Handle success, e.g., close the modal or update the UI
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

// Function to update a category
function updateCategory(categoryId) {
  var name = document.getElementById('update-category-name').value;

  fetch(`/update_category/${categoryId}`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
          'name': name,
      }),
  })
  .then(response => response.json())
  .then(data => {
      console.log(data.message);
      // Handle success, e.g., close the modal or update the UI
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

// Function to delete a task
function deleteTask(taskId) {
    console.log('Deleting task:', taskId);
    if (confirm("Are you sure you want to delete this task?")) {
      fetch(`/delete_task/${taskId}`, {
        method: 'DELETE',
      })
      .then(response => {
        if (response.ok) {
          document.getElementById(`task-${taskId}`).remove(); // Remove task from the DOM
        } else {
          console.error('Error deleting task');
        }
      });
    }
}

// Function to delete a category
function deleteCategory(categoryId) {
    if (confirm("Are you sure you want to delete this category?")) {
      fetch(`/delete_category/${categoryId}`, {
        method: 'DELETE',
      })
      .then(response => {
        if (response.ok) {
          document.getElementById(`category-${categoryId}`).remove(); // Remove category from the DOM
        } else {
          console.error('Error deleting category');
        }
      });
    }
}
