// Create Article
function createArticle() {
    fetch("{% url 'article:create_article' %}", {
        method: "POST",
        body: new FormData(document.querySelector('#ArticleForm')),
    })
    .then(response => refreshArticles())
  
    document.getElementById("ArticleForm").reset(); 
    document.querySelector("[data-modal-toggle='crudModal']").click();
  
    return false;
  }
  
  document.getElementById("ArticleForm").addEventListener("submit", (e) => {
    e.preventDefault();
    createArticle();
  })
  
  // Fetch Articles
  async function getArticles(){
    return fetch("{% url 'article:show_json' %}").then((res) => res.json())
  }
  
  // CRUD Modal
  const modal = document.getElementById('crudModal');
  const modalContent = document.getElementById('crudModalContent');
  
  function showModal() {
      const modal = document.getElementById('crudModal');
      const modalContent = document.getElementById('crudModalContent');
  
      modal.classList.remove('hidden'); 
      setTimeout(() => {
        modalContent.classList.remove('opacity-0', 'scale-95');
        modalContent.classList.add('opacity-100', 'scale-100');
      }, 50); 
  }
  
  function hideModal() {
      const modal = document.getElementById('crudModal');
      const modalContent = document.getElementById('crudModalContent');
  
      modalContent.classList.remove('opacity-100', 'scale-100');
      modalContent.classList.add('opacity-0', 'scale-95');
  
      setTimeout(() => {
        modal.classList.add('hidden');
      }, 150); 
  }
  
  document.getElementById("cancelButton").addEventListener("click", hideModal);
  document.getElementById("closeModalBtn").addEventListener("click", hideModal);
  
  // Refresh Articles
  async function refreshArticles() {
    document.getElementById("article_cards").innerHTML = "";
    document.getElementById("article_cards").className = "";
    const articles = await getArticles();
    let htmlString = "";
    let classNameString = "";
  
    if (articles.length === 0) {
        classNameString = "flex flex-col items-center justify-center min-h-[24rem] p-6";
        htmlString = `
            <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
                <p class="text-center text-gray-600 mt-4">Belum ada data</p>
            </div>
        `;
    }
    else {
      const classNameString = "grid grid-cols-1 gap-6 max-h-[calc(100vh-16rem)] overflow-y-scroll";
  
      function truncateDescription(text, maxWords) {
        const words = text.split(' '); 
        if (words.length > maxWords) {
          return words.slice(0, maxWords).join(' ') + '...'; 
        }
        return text; 
      }
      articles.forEach((item) => {
        const title = DOMPurify.sanitize(item.fields.title);
        const description = DOMPurify.sanitize(item.fields.description);
        const truncatedDescription = truncateDescription(description, 35);
        const image = DOMPurify.sanitize(item.fields.image);
        const id = item.pk;
  
        htmlString += `
        <article class="bg-white p-4 rounded-lg shadow-lg flex flex-col justify-between w-full mb-6">
          <a href="/article/article/${id}">
            <div>
              <img src="/article/media/${image}" alt="${title}" class="w-full h-48 object-cover rounded-md">
              <h3 class="text-xl font-semibold mt-4">${title}</h3>
              <p class="text-gray-600 mt-2">${truncatedDescription}</p>
            </div>
            <div class="flex justify-end mt-6">
              {% if user.is_authenticated and user.username == 'admin' %}
                <a href="/article/edit-article/${item.pk}" >
                <button type="submit" class="bg-white text-yellow-500 border border-yellow-500 px-3 py-1 rounded-lg hover:bg-yellow-500 hover:text-white transition flex items-center mr-2">
                    Edit
                  </button>
                  </svg>
                </a>
                <a href="/article/delete/${item.pk}">
                  <button type="submit" class="bg-white text-red-500 border border-red-500 px-3 py-1 rounded-lg hover:bg-red-500 hover:text-white transition flex items-center">
                    Delete
                  </button>
                </a>
                {% else %}
                <a href="/article/article/${item.pk}">
                    <button type="submit" class="bg-blue-500 text-white px-3 py-1 rounded-lg hover:bg-blue-700 transition flex items-center">
                        View More
                    </button>
                </a>
              {% endif %}
            </div>
          </a>
        </article>
        `;
      });
  
    }
    document.getElementById("article_cards").className = classNameString;
    document.getElementById("article_cards").innerHTML = htmlString;
  }
  refreshArticles();
  
  // Article Card Click Event
  document.addEventListener("DOMContentLoaded", function() {
    const articleCards = document.querySelectorAll('.article-card'); // Pastikan class 'article-card' ada pada card HTML
  
    articleCards.forEach(card => {
      card.addEventListener('click', function() {
        const articleId = this.dataset.id;  // Mengambil ID artikel
        window.location.href = `/article/${articleId}/`;  // Mengarahkan ke URL detail artikel
      });
    });
  });
  
  // Countdown Timer
  const launchDate = new Date("2024-12-31T00:00:00").getTime();
  const countdownFunction = setInterval(() => {
      const now = new Date().getTime();
      const distance = launchDate - now;
  
      const days = Math.floor(distance / (1000 * 60 * 60 * 24));
      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  
      document.getElementById("days").innerHTML = days;
      document.getElementById("hours").innerHTML = hours;
      document.getElementById("minutes").innerHTML = minutes;
  
      if (distance < 0) {
          clearInterval(countdownFunction);
          document.getElementById("countdown").innerHTML = "Launched!";
      }
  }, 1000);
  
  // Subscribe
  const form = document.getElementById('newsletterForm');
    const successMessage = document.getElementById('successMessage'); 
    form.addEventListener('submit', function(event) {
        event.preventDefault();      
        const emailInput = document.getElementById('emailInput').value;     
        if (emailInput) {
            successMessage.classList.remove('hidden'); 
        }
    });