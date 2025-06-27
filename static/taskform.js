document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("taskForm");
  const taskList = document.getElementById("taskList");
  const messageBox = document.getElementById("message");
  const taskIdInput = document.getElementById("task_id");

  // Load tasks on page load
  fetchTasks();

  // Submit handler for create or update
  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const taskData = {
      task_id: taskIdInput.value,
      title: document.getElementById("title").value,
      description: document.getElementById("description").value,
      due_date: document.getElementById("due_date").value,
      priority: document.getElementById("priority").value,
      user_id: document.getElementById("user_id").value || null
    };

    const isUpdate = form.getAttribute("data-update") === "true";
    const method = isUpdate ? "PUT" : "POST";
    const url = isUpdate
      ? `http://localhost:5000/tasks/${taskData.task_id}`
      : "http://localhost:5000/tasks/";

    fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(taskData)
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          messageBox.innerText = "❌ Error: " + data.error;
        } else {
          messageBox.innerText = "✅ " + data.message;
          form.reset();
          form.removeAttribute("data-update");
          taskIdInput.readOnly = false;
          fetchTasks();
        }
      })
      .catch(err => {
        messageBox.innerText = "❌ Failed to send data.";
        console.error("Error:", err);
      });
  });

  function fetchTasks() {
    fetch("http://localhost:5000/tasks/")
      .then(res => res.json())
      .then(data => {
        const tasks = data.tasks || [];
        taskList.innerHTML = "";

        tasks.forEach(task => {
          const li = document.createElement("li");
          li.innerHTML = `
            <strong>${task.title}</strong> (ID: ${task.task_id})<br>
            ${task.description}<br>
            Due: ${task.due_date} | Priority: ${task.priority}<br>
            <button onclick="deleteTask('${task.task_id}')">🗑 Delete</button>
            <button onclick='editTask(${JSON.stringify(task)})'>✏️ Edit</button>
            <hr>`;
          taskList.appendChild(li);
        });
      })
      .catch(err => {
        messageBox.innerText = "❌ Failed to fetch tasks.";
        console.error("Fetch error:", err);
      });
  }

  window.deleteTask = function (taskId) {
    if (!confirm("Are you sure you want to delete this task?")) return;

    fetch(`http://localhost:5000/tasks/${taskId}`, {
      method: "DELETE"
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          messageBox.innerText = "❌ Error: " + data.error;
        } else {
          messageBox.innerText = "✅ " + data.message;
          fetchTasks();
        }
      })
      .catch(err => {
        messageBox.innerText = "❌ Failed to delete task.";
        console.error("Delete error:", err);
      });
  };

  window.editTask = function (task) {
    taskIdInput.value = task.task_id;
    taskIdInput.readOnly = true; // prevent changing ID on update
    document.getElementById("title").value = task.title;
    document.getElementById("description").value = task.description;
    document.getElementById("due_date").value = task.due_date;
    document.getElementById("priority").value = task.priority;
    document.getElementById("user_id").value = task.user_id || "";
    form.setAttribute("data-update", "true");
    messageBox.innerText = "✏️ Editing Task ID: " + task.task_id;
  };
});
