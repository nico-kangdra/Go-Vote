function captureImage() {
  
  fetch("/capture_image").then(
    response => {
      response.json().then(data => ({
        data: data,
        status: response.status
        })
      ).then(res => {
        document.getElementById("cameraImage").src = "data:image/jpeg;base64," + res.data.image_data;
          console.log(res.status, res.data.image_data)
      })
      
        if (response.redirected) {
          window.location = response.url
        } else {
          showLoginError()
        }
    }
)

  

  

  // try {
  //   // Send a request to the server to capture an image
  //   const response = await fetch("/capture_image");

  //   if (!response.ok) {
  //     throw new Error(`HTTP error! Status: ${response.status}`);
  //   }

  //   const data = await response.json();

  //   // Update the image source with the captured image
    
  //   print("y")
  // } catch (error) {
  //   console.error("Error capturing image:", error);
  // }
}
