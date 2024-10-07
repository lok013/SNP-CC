document.addEventListener('DOMContentLoaded', () => {
    fetchUsers();

    document.getElementById('addUserBtn').addEventListener('click', () => {
        const rollNumber = prompt('Enter Roll Number:');
        const name = prompt('Enter Name:');
        const secretPin = prompt('Enter Secret PIN:');
        if (rollNumber && name && secretPin) {
            addUser(rollNumber, name, secretPin);
        }
    });

    document.getElementById('searchBtn').addEventListener('click', () => {
        const rollNumber = document.getElementById('searchInput').value;
        if (rollNumber) {
            searchUser(rollNumber);
        }
    });
});

function fetchUsers() {
    fetch('/api/users')
        .then(response => response.json())
        .then(users => {
            updateTable(users);
        })
        .catch(error => {
            console.error('Error fetching users:', error);
        });
}

function searchUser(rollNumber) {
    fetch(`/api/users/search/${rollNumber}`)
        .then(response => response.json())
        .then(user => {
            updateTable(user ? [user] : []);
        })
        .catch(error => {
            console.error('Error searching user:', error);
        });
}

function updateTable(users) {
    const userTableBody = document.getElementById('userTableBody');
    userTableBody.innerHTML = '';
    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.roll_number}</td>
            <td>${user.name}</td>
            <td>${user.secret_pin}</td>
            <td><button onclick="deleteUser('${user.roll_number}')">Delete</button></td>
            <td><button class="modify-btn" onclick="modifyUser('${user.roll_number}')">Modify</button></td>
        `;
        userTableBody.appendChild(row);
    });
}

function deleteUser(rollNumber) {
    fetch(`/api/users/${rollNumber}`, {
        method: 'DELETE'
    })
    .then(() => {
        fetchUsers(); // Refresh the user list
    })
    .catch(error => {
        console.error('Error deleting user:', error);
    });
}

function addUser(rollNumber, name, secretPin) {
    fetch('/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ roll_number: rollNumber, name: name, secret_pin: secretPin })
    })
    .then(() => {
        fetchUsers(); // Refresh the user list
    })
    .catch(error => {
        console.error('Error adding user:', error);
    });
}

function modifyUser(rollNumber) {
    window.location.href = `/modify/${rollNumber}`;
}

