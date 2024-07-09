
// Navigation bar animation
let topBar = document.querySelector('.top-bar')
let midBar = document.querySelector('.mid-bar')
let bottomBar = document.querySelector('.bottom-bar')
let nav = document.querySelector('.menu-bar')
document.querySelector('.nav-toggle').addEventListener('click', ()=>{
    topBar.classList.toggle('rotate')
    bottomBar.classList.toggle('rotate')
    midBar.classList.toggle('hidden')
    nav.classList.toggle('visible')
})

// Post request
const form = document.getElementById("timeline-form")

form.addEventListener('submit',function(e){
    e.preventDefault()
    const payload = new FormData(form);
    fetch('/api/timeline_post', {
        method: 'POST',
        body: payload,
        })
        .then(res => res.json())
        .then(data => {console.log(data)
            location.reload()
        }
    ) 
})