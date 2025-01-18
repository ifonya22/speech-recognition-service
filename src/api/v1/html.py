# content = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>File Upload</title>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             padding: 20px;
#         }
#         .upload-container {
#             border: 2px dashed #ccc;
#             border-radius: 10px;
#             padding: 20px;
#             text-align: center;
#             margin-bottom: 20px;
#             width: 300px;
#         }
#         .upload-container.dragover {
#             background-color: #f0f0f0;
#         }
#         #output {
#             margin-top: 20px;
#         }
#         .hidden {
#             display: none;
#         }
#         #fileName {
#             margin-top: 10px;
#             font-style: italic;
#             color: #555;
#         }
#     </style>
# </head>
# <body>
#     <h1>Upload and Transcribe</h1>

#     <form id="uploadForm" enctype="multipart/form-data">
#         <div class="upload-container" id="dropArea">
#             <p>Drag and drop a file here or click to upload</p>
#             <input type="file" id="fileInput" name="file" class="hidden">
#             <p id="fileName"></p>
#         </div>

#         <label for="modelSelect">Select a model:</label>
#         <select id="modelSelect" name="model">
#             <!-- Options will be dynamically populated -->
#         </select>

#         <button type="submit">Upload and Transcribe</button>
#     </form>

#     <div id="output"></div>

#     <script>
#         const dropArea = document.getElementById('dropArea');
#         const fileInput = document.getElementById('fileInput');
#         const modelSelect = document.getElementById('modelSelect');
#         const uploadForm = document.getElementById('uploadForm');
#         const output = document.getElementById('output');
#         const fileNameDisplay = document.getElementById('fileName');

#         // Fetch model list
#         fetch('http://localhost:8000/api/v1/models/required_vram')
#             .then(response => response.json())
#             .then(models => {
#                 for (const [model, size] of Object.entries(models)) {
#                     const option = document.createElement('option');
#                     option.value = model;
#                     option.textContent = `${model} (${size})`;
#                     modelSelect.appendChild(option);
#                 }
#             });

#         // Drag and drop handling
#         dropArea.addEventListener('dragover', (event) => {
#             event.preventDefault();
#             dropArea.classList.add('dragover');
#         });

#         dropArea.addEventListener('dragleave', () => {
#             dropArea.classList.remove('dragover');
#         });

#         dropArea.addEventListener('drop', (event) => {
#             event.preventDefault();
#             dropArea.classList.remove('dragover');
#             const files = event.dataTransfer.files;
#             if (files.length > 0) {
#                 fileInput.files = files;
#                 fileNameDisplay.textContent = `Selected file: ${files[0].name}`;
#             }
#         });

#         dropArea.addEventListener('click', () => {
#             fileInput.click();
#         });

#         fileInput.addEventListener('change', () => {
#             if (fileInput.files.length > 0) {
#                 fileNameDisplay.textContent = `Selected file: ${fileInput.files[0].name}`;
#             }
#         });

#         // Form submission
#         uploadForm.addEventListener('submit', (event) => {
#             event.preventDefault();

#             const formData = new FormData();
#             const file = fileInput.files[0];
#             const model = modelSelect.value;

#             if (!file || !model) {
#                 alert('Please select a file and a model!');
#                 return;
#             }

#             formData.append('file', file);

#             fetch(`http://localhost:8000/api/v1/transcribe?model=${model}`, {
#                 method: 'POST',
#                 body: formData,
#             })
#                 .then(response => response.json())
#                 .then(data => {
#                     const text = data.text;

#                     output.innerHTML = `
#                         <p>Transcription:</p>
#                         <textarea readonly rows="5" cols="40">${text}</textarea>
#                         <br>
#                         <a href="data:text/plain;charset=utf-8,${encodeURIComponent(text)}" download="transcription.txt">
#                             <button>Download Text</button>
#                         </a>
#                     `;
#                 })
#                 .catch(error => {
#                     console.error('Error:', error);
#                     alert('An error occurred while transcribing the file.');
#                 });
#         });
#     </script>
# </body>
# </html>

# """
content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Upload and Transcription</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        .upload-container {
            border: 2px dashed #ccc;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
            width: 300px;
        }
        .upload-container.dragover {
            background-color: #f0f0f0;
        }
        #output {
            margin-top: 20px;
            width: 100%;
            max-width: 600px;
        }
        .hidden {
            display: none;
        }
        #fileName {
            margin-top: 10px;
            font-style: italic;
            color: #555;
        }
        textarea {
            width: 100%;
            resize: none;
        }
    </style>
</head>
<body>
    <h1>Stream Audio Transcription</h1>

    <form id="uploadForm">
        <div class="upload-container" id="dropArea">
            <p>Drag and drop a file here or click to upload</p>
            <input type="file" id="fileInput" name="file" class="hidden">
            <p id="fileName"></p>
        </div>

        <label for="modelSelect">Select a model:</label>
        <select id="modelSelect" name="model"></select>

        <button type="submit">Start Transcription</button>
    </form>

    <div id="output">
        <p id="status">Waiting for file upload...</p>
        <textarea id="transcriptionOutput" rows="10"
        <textarea id="transcriptionOutput" rows="10" readonly></textarea>
        <br>
        <a id="downloadLink" href="#" download="transcription.txt" class="hidden">
            <button id="downloadButton" class="hidden">Download Text</button>
        </a>
    </div>

    <script>
        const dropArea = document.getElementById('dropArea');
        const fileInput = document.getElementById('fileInput');
        const modelSelect = document.getElementById('modelSelect');
        const uploadForm = document.getElementById('uploadForm');
        const status = document.getElementById('status');
        const transcriptionOutput = document.getElementById('transcriptionOutput');
        const downloadLink = document.getElementById('downloadLink');
        const downloadButton = document.getElementById('downloadButton');
        const fileNameDisplay = document.getElementById('fileName');

        // Fetch model list
        fetch('http://localhost:8000/api/v1/models/required_vram')
            .then(response => response.json())
            .then(models => {
                for (const [model, size] of Object.entries(models)) {
                    const option = document.createElement('option');
                    option.value = model;
                    option.textContent = `${model} (${size})`;
                    modelSelect.appendChild(option);
                }
            });

        // Drag and drop handling
        dropArea.addEventListener('dragover', (event) => {
            event.preventDefault();
            dropArea.classList.add('dragover');
        });

        dropArea.addEventListener('dragleave', () => {
            dropArea.classList.remove('dragover');
        });

        dropArea.addEventListener('drop', (event) => {
            event.preventDefault();
            dropArea.classList.remove('dragover');
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                fileNameDisplay.textContent = `Selected file: ${files[0].name}`;
            }
        });

        dropArea.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                fileNameDisplay.textContent = `Selected file: ${fileInput.files[0].name}`;
            }
        });

        // WebSocket implementation for real-time transcription
uploadForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const file = fileInput.files[0];
    const model = modelSelect.value;

    if (!file || !model) {
        alert('Please select a file and a model!');
        return;
    }

    status.textContent = 'Connecting to server...';

    // Создание WebSocket подключения
    const socket = new WebSocket(`ws://localhost:8000/api/v1/ws/transcribe?model=${model}`);

    socket.onopen = () => {
        status.textContent = 'Uploading file...';

        // Отправляем метаданные файла
        const metadata = { model, filename: file.name };
        socket.send(JSON.stringify(metadata));

        // Читаем файл как ArrayBuffer
        const reader = new FileReader();
        reader.onload = (e) => {
            const arrayBuffer = e.target.result;

            // Отправляем файл в бинарном формате
            socket.send(arrayBuffer);
        };

        reader.readAsArrayBuffer(file);
    };

    socket.onmessage = (event) => {
        console.log(event.data);
        const data = JSON.parse(event.data);
        console.log(data.type);

        // Отображаем прогресс
        if (data.type === 'progress') {
            status.textContent = `Progress: ${data.progress}%`;
        }
        // Обрабатываем транскрипцию
        else if (data.type === 'transcription') {
            transcriptionOutput.value += `${data.text}\n`;  // Обновляем текстовое поле
        }
        // Обработка завершения
        else if (data.type === 'done') {
            status.textContent = 'Transcription completed!';
            // Подготовка ссылки для скачивания
            downloadLink.href = `data:text/plain;charset=utf-8,${encodeURIComponent(transcriptionOutput.value)}`;
            downloadButton.classList.remove('hidden');
            downloadLink.classList.remove('hidden');
        }
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        status.textContent = 'An error occurred. Please try again.';
    };

    socket.onclose = () => {
        status.textContent = 'Connection closed.';
    };
});
    </script>
</body>
</html>
"""
