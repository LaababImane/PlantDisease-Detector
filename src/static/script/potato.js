async function predictPotato() {
  const thisForm = document.getElementById('myForm');
  var thisFile = document.getElementById('file1');
  var name = thisFile.files[0]
  var formdata = new FormData();
  formdata.append("file", name);

  var requestOptions = {
      method: 'POST',
      body: formdata,
      redirect: 'follow',
    };
    try{
    const response = await fetch("http://localhost:8000/predictPotato", requestOptions)
    var data = await response.json();
    document.getElementById("disease").innerHTML = data.class
    document.getElementById("cause").innerHTML = data.cause
    document.getElementById("dis").innerHTML = data.dispcription
    document.getElementById("treat").innerHTML = data.treatment
    document.getElementById("prevention").innerHTML = data.prevention 
  } catch (error) {
    console.error(error);
    document.getElementById("error").innerHTML = "Error parsing response data.";
  }
      fetch("/equalize_image", {
        method: "POST",
        body: formdata
      })
      .then(response => response.blob())
      .then(blob => {
        // Create a data URL from the blob data
        const data_url = URL.createObjectURL(blob);
        // Set the src attribute of the result image element
        document.getElementById("Equalize-image").setAttribute("src", data_url);
      });

      fetch("/detect_edges", {
        method: "POST",
        body: formdata
      })
      .then(response => response.blob())
      .then(blob => {
        // Create a data URL from the blob data
        const data_url = URL.createObjectURL(blob);
        // Set the src attribute of the result image element
        document.getElementById("edge_detection-image").setAttribute("src", data_url);
      });
      fetch("/histogram_equalization", {
        method: "POST",
        body: formdata
      })
      .then(response => response.blob())
      .then(blob => {
        // Create a data URL from the blob data
        const data_url = URL.createObjectURL(blob);
        // Set the src attribute of the result image element
        document.getElementById("histogram_equalization-image").setAttribute("src", data_url);
      });

      // fetch('/equalize', {
      //   method: "POST",
      //   body: formdata
      // })
      // .then(response => response.blob())
      // .then(blob => {
      //   // Create a data URL from the blob data
      //   const data_url = URL.createObjectURL(blob);
      //   // Set the src attribute of the result image element
      //   document.getElementById("histogram-image").setAttribute("src", data_url);
      // });

  }


    var loadFile = function(event) {
      var output = document.getElementById('img');
      output.src = URL.createObjectURL(event.target.files[0]);
      output.onload = function() {
        URL.revokeObjectURL(output.src) // free memory
      }
    };


    function ul(index) {
      console.log('click!' + index)
      
      var underlines = document.querySelectorAll(".underline");
    
      for (var i = 0; i < underlines.length; i++) {
        underlines[i].style.transform = 'translate3d(' + index * 100 + '%,0,0)';
      }
    }



