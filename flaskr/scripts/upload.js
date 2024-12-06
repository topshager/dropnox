document.getElementById('uploadForm').addEventListener('submit',async(event) =>{
  event.preventDefault();

  const folderInput = document.getElementById('folderInput');
  const files = folderInput.files;
  const formData = new FormData();

  if (files.length == 0){
    alert('Please select a folder to upload.');
    return;
  }
  for(const file of files){
    formData.append('files',file,file.file.webkitRelativePath)
  }
  try{
    
  }
})
