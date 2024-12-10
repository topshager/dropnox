document.addEventListener('DOMContentLoaded', () => {
  const items = document.querySelectorAll('.file, .folder');
  const folders = document.querySelectorAll('.folder');

  let draggedItem = null;

  // Set up dragstart and dragend events
  items.forEach(item => {
    item.setAttribute('draggable', true);

    item.addEventListener('dragstart', (event) => {
      draggedItem = event.target;
      event.dataTransfer.setData('text/plain', event.target.id);
      setTimeout(() => draggedItem.style.display = 'none', 0);
    });

    item.addEventListener('dragend', () => {
      setTimeout(() => draggedItem.style.display = 'block', 0);
      draggedItem = null;
    });
  });

  // Set up dragover, dragenter, and drop events for folders
  folders.forEach(folder => {
    folder.addEventListener('dragover', (event) => {
      event.preventDefault();
      folder.classList.add('dragover');
    });

    folder.addEventListener('dragleave', () => {
      folder.classList.remove('dragover');
    });

    folder.addEventListener('drop', (event) => {
      event.preventDefault();
      folder.classList.remove('dragover');

      const draggedId = event.dataTransfer.getData('text/plain');
      const draggedElement = document.getElementById(draggedId);

      if (draggedElement) {
        folder.appendChild(draggedElement);
      }
    });
  });
});
