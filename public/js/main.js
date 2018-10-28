
function getCodes(category) {

    mainDiv = document.getElementById("main");
    mainDiv.style.display = 'none';

    const url = 'http://localhost:9090/'+category

    fetch(url,{
        headers: {
            'Accept': 'application/json',
          },
    })
        .then( response => {
            console.log(response.status)
            return response.json()
        })
        .then( parsedJson =>{
            this.color = 0;
            this.codesDiv = document.getElementById("codes");
            for(code in parsedJson['codes']){
                div = document.createElement('div');
                par = document.createElement('p');

                if(this.color == 0){
                    div.classList.add('code-plate-1')
                }else {
                    div.classList.add('code-plate-2')
                }
                this.color = (this.color + 1)%2;

                div.id = parsedJson['codes'][code];
                div.onclick = (ev) => {
                  getCodeDetails(ev.target.id)
                };

                par.classList.add('main-text');
                par.innerText = parsedJson['codes'][code];

                div.appendChild(par);
                this.codesDiv.appendChild(div)
            }
            this.codesDiv.style.display = 'flex'
        })

}

function getCodeDetails(codeName) {
     codesDiv = document.getElementById("codes");
     codesDiv.style.display = 'none';

    const url = 'http://localhost:9090/code_details';
    console.log(codeName);

    fetch(url,{
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
          },
          body: JSON.stringify({
            module_name: codeName,
          })
        })
        .then( response => {
            console.log(response.status);
            return response.json()
        })
        .then( parsedJson =>{
            console.log(parsedJson['description'], parsedJson['name'])
            this.codeDiv = document.getElementById("code")
            this.codeDiv.style.display = 'flex'
        })
}