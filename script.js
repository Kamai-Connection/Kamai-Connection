function openModal(url) {
    fetch(url)
      .then(response => response.text())
      .then(html => {
        document.getElementById('modalContainer').innerHTML = html;
        document.querySelector('.modal').style.display = 'block';
        if (url === '/display_workers') {
          fetch('/get_workers')
            .then(response => response.json())
            .then(data => {
              const workersList = document.getElementById('workersList');
              workersList.innerHTML = '';
              data.forEach(worker => {
                const li = document.createElement('li');
                li.textContent = `Name: ${worker.name}, Skills: ${worker.skills.join(', ')}`;
                workersList.appendChild(li);
              });
            });
        } else if (url === '/display_ratings') {
          fetch('/get_ratings')
            .then(response => response.json())
            .then(data => {
              const ratingsList = document.getElementById('ratingsList');
              ratingsList.innerHTML = '';
              data.forEach(rating => {
                const li = document.createElement('li');
                li.textContent = rating;
                ratingsList.appendChild(li);
              });
            });
        } else if (url === '/find_jobs') {
          fetch('/get_workers')
            .then(response => response.json())
            .then(data => {
              const workerSelect = document.getElementById('workerSelect');
              workerSelect.innerHTML = '<option value="">Select a worker</option>';
              data.forEach(worker => {
                const option = document.createElement('option');
                option.value = worker.name;
                option.textContent = worker.name;
                workerSelect.appendChild(option);
              });
            });
        }
      });
  }
  
  function closeModal() {
    document.querySelector('.modal').style.display = 'none';
  }
  
  function saveWorker() {
    const form = document.getElementById('workerForm');
    const formData = new FormData(form);
    fetch('/register_worker', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
      closeModal();
    });
  }
  
  function findMatches() {
    const workerSelect = document.getElementById('workerSelect');
    const selectedWorker = workerSelect.value;
  
    if (!selectedWorker) {
      alert('Please select a worker.');
      return;
    }
  
    fetch('/find_matches', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ worker: selectedWorker })
    })
    .then(response => response.json())
    .then(data => {
      const matchResult = document.getElementById('matchResult');
      matchResult.innerHTML = '';
      if (data.length > 0) {
        data.forEach(businessman => {
          const div = document.createElement('div');
          div.innerHTML = `<p>Name: ${businessman.name}, Contact: ${businessman.contact}, Work Needed: ${businessman.work_needed}</p>`;
          matchResult.appendChild(div);
        });
      } else {
        matchResult.textContent = 'No suitable businessmen found for this worker.';
      }
    });
  }
  document.addEventListener('DOMContentLoaded', function () {
    const modalButtons = document.querySelectorAll('[data-modal-target]');
    const modalContainer = document.getElementById('modalContainer');

    modalButtons.forEach(button => {
        button.addEventListener('click', function () {
            const targetModal = this.getAttribute('data-modal-target');
            openModal(targetModal);
        });
    });

    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        modalContainer.innerHTML = '';
        modalContainer.appendChild(modal);
        modal.style.display = 'block';
    }

    function closeModal() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.style.display = 'none';
        });
    }

    window.onclick = function (event) {
        const modals = document.querySelectorAll('.modal');
        if (event.target.classList.contains('modal')) {
            modals.forEach(modal => {
                modal.style.display = 'none';
            });
        }
    };

    // Redirect to registration forms when clicking register buttons
    const registerWorkerBtn = document.getElementById('registerWorkerBtn');
    const registerBusinessmanBtn = document.getElementById('registerBusinessmanBtn');

    registerWorkerBtn.addEventListener('click', function () {
        window.location.href = '/register_worker';
    });

    registerBusinessmanBtn.addEventListener('click', function () {
        window.location.href = '/register_businessman';
    });
});
document.getElementById('findJobOffersForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const selectedWorker = document.getElementById('selectedWorker').value;
    fetch('/find_job_offers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ selectedWorker: selectedWorker }),
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('jobOffersResult').innerHTML = data;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

