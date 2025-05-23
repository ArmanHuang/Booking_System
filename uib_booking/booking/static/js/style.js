const profileImage = document.getElementById('profileImage');
const imageModal = document.getElementById('imageModal');
const modalImage = document.getElementById('modalImage');

profileImage.addEventListener('click', () => {
    modalImage.src = profileImage.src;
    imageModal.classList.remove('opacity-0', 'pointer-events-none');
});

imageModal.addEventListener('click', () => {
    imageModal.classList.add('opacity-0', 'pointer-events-none');
});


