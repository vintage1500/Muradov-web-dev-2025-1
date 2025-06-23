function openDeleteModal(animalId, animalName) {
    const modal = document.getElementById('deleteModal');
    const text = document.getElementById('deleteText');
    const form = document.getElementById('deleteForm');

    text.textContent = `Вы уверены, что хотите удалить животное ${animalName}?`;
    form.action = `/animals/${animalId}/delete`;  // выставляем action
    modal.classList.remove('hidden');
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.add('hidden');
}