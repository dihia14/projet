const dropContainer = document.getElementById("dropContainer");
const fileInput = document.getElementById("fileInput");

dropContainer.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropContainer.classList.add("drag-over");
});

dropContainer.addEventListener("dragleave", () => {
    dropContainer.classList.remove("drag-over");
});

dropContainer.addEventListener("drop", (e) => {
    e.preventDefault();
    dropContainer.classList.remove("drag-over");
    const files = e.dataTransfer.files;
    uploadFiles(files);
});

dropContainer.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", (e) => {
    const files = e.target.files;
    uploadFiles(files);
});



function uploadFiles(files) {
    //const user_id = "example_user1"; //changer une fois session activee , yes mettre la seconde ligne : ?  
    // const user_id = document.getElementById("user_id").value;
    const user_id = document.getElementById("user_id").value; 
    

    const formData = new FormData();
    formData.append("user_id", user_id);

    for (let file of files) {
        formData.append("files", file);
    }

    fetch("upload", {
        method: "POST",
        body: formData,
    })

    .then((response) => response.json())       

    .then((data) => {

        if (data.files) {
            alert("Fichiers téléchargés avec succès !");
            updateFileTable(data.files);
            
        } else {
            alert("Erreur lors de l'upload des fichiers : " + data.error);
        }
    })
    .catch((error) => {
        console.error("Erreur lors de l'upload :", error);
    });
}



function updateFileTable(files) {
    const tableBody = document.querySelector("tbody");
    tableBody.innerHTML = ""; 
    files.forEach((file) => {
        const row = document.createElement("tr");
        row.className = "border-b border-gray-200 hover:bg-gray-100";

        row.innerHTML = `
        <td class="py-3 px-6">
            <a href="/download/example_user1/${file}" class="text-blue-500 hover:underline" download="${file}">
                ${file}
            </a>
        </td>
        <td class="py-3 px-6">
            <form action="/delete_file" method="POST">
                <input type="hidden" name="user_id" value="example_user1" />
                <input type="hidden" name="file_name" value="${file}" />
                <button type="submit" class="text-red-500 hover:underline">Supprimer</button>
            </form>
        </td>
        `;

        tableBody.appendChild(row);
    });
}



// function updateFileTable(files) {
//     const user_id = document.getElementById("user_id").value; // recup dynamiquement user_id
//     const tableBody = document.querySelector("tbody");
//     tableBody.innerHTML = ""; 
//     files.forEach((file) => {
//         const row = document.createElement("tr");
//         row.className = "border-b border-gray-200 hover:bg-gray-100";

//         row.innerHTML = `
//         <td class="py-3 px-6">
//             <a href="/download/${user_id}/${file}" class="text-blue-500 hover:underline" download="${file}">
//                 ${file}
//             </a>
//         </td>
//         <td class="py-3 px-6">
//             <form action="/delete_file" method="POST">
//                 <input type="hidden" name="user_id" value="${user_id}" />
//                 <input type="hidden" name="file_name" value="${file}" />
//                 <button type="submit" class="text-red-500 hover:underline">Supprimer</button>
//             </form>
//         </td>
//         `;

//         tableBody.appendChild(row);
//     });
// }
