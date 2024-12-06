document.getElementById('uploadForm').addEventListener('submit',async(event) =>{
  event.preventDefault();

  const folderInput = document.getElementById('folderInput');
  const files = folderInput.files;
  const formData = new FormData();
  if (!files || files.length === 0) {
    alert('Please select a folder to upload.');
    return;
}

  for (const file of files){
    if (file.webkitRelativePath){
      console.log(file.webkitRelativePath);
      formData.append('files',file,file.webkitRelativePath);
    }
    else{
      console.error('File does not have webkitRelativePath:', file);
    }
  }


  if (files.length == 0){
    alert(`Please select a folder to upload.`);
    return;

  }
  try{
    const response =  await fetch ('/upload-folder', {
      method :'POST',
      body: formData,
    });
    if (response.ok){
      alert(`Folder uploaded successfully!`);
    }else{
      const  errorData = await response.json();
      alert(`Error: ${errorData.message}`)
    }
  }catch (error){
    console.error()
    console.error(`Error uploading folder:`, error);
    alert(`An error occurred during upload.`);
  }
});
