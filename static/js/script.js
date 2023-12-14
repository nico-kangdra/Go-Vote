async function captureImage() {
  try {
    // Send a request to the server to capture an image
    const response = await fetch("/capture_image");

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    // Update the image source with the captured image
    document.getElementById("cameraImage").src =
      "data:image/jpeg;base64," + data.image_data;
  } catch (error) {
    console.error("Error capturing image:", error);
  }
}
