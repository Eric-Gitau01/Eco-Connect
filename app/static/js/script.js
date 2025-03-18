const API_URL = "http://127.0.0.1:5000/api";

// Function to load issues from the backend
function loadIssues() {
    fetch(`${API_URL}/issues`)
        .then(response => {
            if (!response.ok) {
                throw new Error("HTTP error !! " + response.status);
        }
        return response.json();
    })
        .then(issues => {
            console.log("Fetch issues:", issues);
            $("#issuesContainer").html("");
            issues.forEach(issue => {
                $("#issuesContainer").append(`
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">${issue.title}</h5>
                                <p><strong>Location:</strong> ${issue.location}</p>
                                <p class="card-text">${issue.description}</p>
                                <button class="btn btn-primary btn-sm" onclick="showCommentBox(${issue.id})">Add Comment</button>
                                <div id="commentBox-${issue.id}" style="display: none;">
                                    <textarea id="commentText-${issue.id}" class="form-control" rows="2" placeholder="Write a comment..."></textarea>
                                    <button class="btn btn-success btn-sm mt-2" onclick="submitComment(${issue.id})">Submit</button>
                                </div>
                                <h6 class="mt-2">Comments:</h6>
                                <ul id="comments-${issue.id}" class="list-group">
                                    ${issue.comments.map(comment => `<li class="list-group-item">${comment.text}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                `);
            });
        })
        .catch(error => console.error("Error fetching issues:", error));
}

// Function to submit an issue
$("#reportForm").on("submit", function(event) {
    event.preventDefault();

    const title = $("#issueTitle").val();
    const location = $("#issueLocation").val();
    const description = $("#issueDescription").val();

    fetch(`${API_URL}/issues`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, location, description })
    })
    .then(response => response.json())
    .then(data => {
        alert("Issue reported successfully!");
        window.location.href = "index.html";
    })
    .catch(error => console.error("Error reporting issue:", error));
});

// Show the comment box for a specific issue
function showCommentBox(issueId) {
    $(`#commentBox-${issueId}`).toggle();
}

// Function to submit a comment
function submitComment(issueId) {
    const commentText = $(`#commentText-${issueId}`).val();
    if (!commentText) {
        alert("Comment cannot be empty.");
        return;
    }

    fetch(`${API_URL}/comments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ issue_id: issueId, text: commentText })
    })
    .then(response => response.json())
    .then(data => {
        alert("Comment added successfully!");
        loadIssues();
    })
    .catch(error => console.error("Error posting comment:", error));
}

// Load issues on page load
$(document).ready(function() {
    loadIssues();
});
// Login Function
$("#loginForm").on("submit", function(event) {
    event.preventDefault();

    const username = $("#username").val();
    const password = $("#password").val();

    fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem("token", data.access_token);
            alert("Login successful!");
            window.location.href = "index.html";
        } else {
            alert("Invalid credentials. Please try again.");
        }
    })
    .catch(error => console.error("Error logging in:", error));
});
