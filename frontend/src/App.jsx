import { useState, useEffect } from "react"

function App() {

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [tasks, setTasks] = useState([])
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [loggedIn, setLoggedIn] = useState(false)

  const API = "http://127.0.0.1:8000"

  const getToken = () => localStorage.getItem("token")

  const login = async () => {
    const res = await fetch(`${API}/auth/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    })

    const data = await res.json()

if (data.access_token) {
  localStorage.setItem("token", data.access_token)
  setLoggedIn(true)
  getTasks()
} else {
  alert("Login failed")
}
    setLoggedIn(true)

    getTasks()
  }

  const logout = () => {
    localStorage.removeItem("token")
    setLoggedIn(false)
    setTasks([])
  }

  const getTasks = async () => {
    const res = await fetch(`${API}/tasks`, {
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    })

    const data = await res.json()
    setTasks(data)
  }

  const createTask = async () => {
     if (!title.trim()) {
    alert("Task title cannot be empty")
    return
   }


    await fetch(`${API}/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`
      },
      body: JSON.stringify({
        title,
        description
      })
    })

    setTitle("")
    setDescription("")
    getTasks()
  }

  const deleteTask = async (id) => {

    await fetch(`${API}/tasks/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    })

    getTasks()
  }

  const toggleComplete = async (task) => {

    await fetch(`${API}/tasks/${task.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`
      },
      body: JSON.stringify({
        title: task.title,
        description: "",
        completed: !task.completed
      })
    })

    getTasks()
  }

  const updateTask = async (task) => {

    const newTitle = prompt("Update task title", task.title)

    if (!newTitle) return

    await fetch(`${API}/tasks/${task.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`
      },
      body: JSON.stringify({
        title: newTitle,
        description: "",
        completed: task.completed
      })
    })

    getTasks()
  }

  useEffect(() => {
    if (getToken()) {
      setLoggedIn(true)
      getTasks()
    }
  }, [])

  if (!loggedIn) {
    return (
      <div style={{ padding: 40 }}>
        <h1>Todo App</h1>

        <h2>Login</h2>

        <input
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <br /><br />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <br /><br />

        <button onClick={login}>Login</button>
      </div>
    )
  }

  return (
    <div style={{ padding: 40 }}>

      <h1>Todo App</h1>

      <button onClick={logout}>Logout</button>

      <hr />

      <h2>Create Task</h2>

      <input
  placeholder="Task title"
  value={title}
  onChange={(e) => setTitle(e.target.value)}
/>

<br /><br />

<input
  placeholder="Task description"
  value={description}
  onChange={(e) => setDescription(e.target.value)}
 />

 <br /><br />

 <button onClick={createTask}>Add Task</button>

      <hr />

      <h2>Your Tasks</h2>

      {tasks.map((task) => (
        <div key={task.id} style={{
          border: "1px solid gray",
          padding: 10,
          marginBottom: 10
        }}>

          <b>{task.title}</b>
          <p style={{color: "#1391df"}}>{task.description}</p>   
         <p>Status: {task.completed ? "✅ Completed" : "❌ Pending"}</p>

          <button onClick={() => toggleComplete(task)}>
            Toggle Complete
          </button>

          <button onClick={() => updateTask(task)}>
            Update
          </button>

          <button onClick={() => deleteTask(task.id)}>
            Delete
          </button>

        </div>
      ))}

    </div>
  )
}

export default App