
currentCategory= '';
currentCode = '';
currentData = '';
waitResponse = false;


function getCodes(category) {

    document.getElementById("main").style.display = 'none';
    document.getElementById("bottom").style.display = 'flex';

    currentCategory = category;

    const url = 'http://localhost:9090/'+category;

    fetch(url,{
        headers: {
            'Accept': 'application/json',
          },
    })
        .then( response => {
            console.log(response.status);
            return response.json()
        })
        .then( parsedJson =>{
            this.color = 0;
            this.codesDiv = document.getElementById("codes");
            clear(this.codes);
            for(code in parsedJson['codes']){
                div = document.createElement('div');
                par = document.createElement('p');

                if(this.color === 0){
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

    document.getElementById("codes").style.display = 'none';


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
            console.log(parsedJson['description'], parsedJson['name']);
            this.codeDiv = document.getElementById("code");
            this.codeDiv.style.display = 'flex';
            this.theory= document.getElementById("theory");
            clear(this.theory);
            this.theory.innerHTML = parsedJson['description'];
            currentCode = codeName;

        })
}

function beginTest() {

    if(currentCode===''&&!waitResponse) {
        waitResponse=true;
        setTimeout(beginTest, 200);
    }
    document.getElementById("code").style.display = 'none';

    const url = 'http://localhost:9090/encodedata';
    fetch(url,{
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
          },
          body: JSON.stringify({
            module_name: currentCode,
          })
        })
        .then( response => {
            console.log(response.status);
            return response.json()
        })
        .then( parsedJson =>{
            console.log(parsedJson['data'], parsedJson['view']);
            this.taskDiv = document.getElementById("task");
            clear(this.taskDiv);
            this.taskDiv.innerHTML = parsedJson['view'];
            document.getElementById("test").style.display = 'flex';
            currentData=parsedJson['data']['message']
        })
}

function check(){

    const url = 'http://localhost:9090/encoderesult';
    fetch(url,{
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
          },
          body: JSON.stringify({
              'module_name': currentCode,
              'data':currentData,
              'answer': document.getElementById("answer").value
          })
        })
        .then( response => {
            console.log(response.status);
            return response.json()
        })
        .then( parsedJson =>{
            console.log(parsedJson);
            if(parsedJson['result']){
                document.getElementById('trueAnswer').style.display='block';
                 setTimeout(goBack, 1400);
            }
        })
}


function goBack() {
    if(document.getElementById("code").style.display==='flex'){
        document.getElementById("code").style.display='none';
        getCodes(currentCategory)
    }else if(document.getElementById("codes").style.display==='flex'){
        document.getElementById("codes").style.display='none';
        document.getElementById("main").style.display='flex';
        document.getElementById("bottom").style.display = 'none';
        currentCategory=''
    }else if(document.getElementById("test").style.display==='flex'){
        document.getElementById("test").style.display='none';

        document.getElementById("bottom").style.display = 'flex';
        currentData='';
        getCodeDetails(currentCode)
    }

}

function clear(div) {
    div.innerHTML = ''
}