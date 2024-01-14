function syncALLgraph(){
    document.querySelectorAll("div.graphviewer").forEach((graphviewer)=>{ syncgraph(graphviewer)});
    }
    function syncgraph(graphviewer){
        var svgObject = document.getElementById('svgObject');
        var svgUrl = graphviewer.getAttribute("name")
        
        // Erstelle ein neues SVG-Objekt
        var newSvgObject = document.createElement('object');
        newSvgObject.type = "image/svg+xml";
        newSvgObject.data = svgUrl;
        newSvgObject.classList.add('graphsvg', 'loading');
    
        newSvgObject.onload = function() {
            this.classList.remove('loading');
            var box = this.parentElement;
            
            while (box.childElementCount>1){
                
                box.removeChild(box.firstChild);
            }
    
            console.log(box.firstChild);
        };
    
    
        graphviewer.appendChild(newSvgObject);
        console.log("request")
    }
    
    setInterval(syncALLgraph, 1*60*1000)
    syncALLgraph()