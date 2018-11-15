
currentCategory= '';
currentCode = '';
currentData = '';

currenteEncoderEndpoit = '';
currenteResultEndpoit = '';

currentStep = 0;
currentGenerator =  0;
stepsTask = false;

generators= null;
steps = null;

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


    const url = 'http://localhost:9090/codedetails';
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

            console.log(parsedJson);
            this.codeDiv = document.getElementById("code");
            this.codeDiv.style.display = 'flex';
            this.theory= document.getElementById("theory");
            clear(this.theory);
            this.theory.innerHTML = parsedJson['description'];

<<<<<<< HEAD
            console.log(parsedJson["details"]["generators"])
            if(parsedJson["details"]["generators"]!=undefined){
=======
            if(parsedJson["details"]["generators"] !== undefined){
>>>>>>> 7dbf3b701ba287ff529842ffac3d2cce97a43e38
                generators = parsedJson["details"]["generators"];
                steps = parsedJson["details"]["steps"];
                stepsTask = true;
                currentGenerator = 0;
                currentStep = 0;
            }

            currentCode = codeName;

        })
}

function beginTest() {

    if(currentCode===''&&!waitResponse) {
        waitResponse=true;
        setTimeout(beginTest, 100);
    }

    document.getElementById("code").style.display = 'none';

    if(stepsTask){
        currenteEncoderEndpoit = "stepgenerators";
    }
    else {
        currenteEncoderEndpoit = "encodedata";
    }


    const url = 'http://localhost:9090/'+currenteEncoderEndpoit;
    fetch(url,{
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
          },
          body: JSON.stringify({
              module_name: currentCode,
              step: steps!=null?steps[currentStep]:'',
              generator: generators!=null?generators[currentGenerator]:''
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
            currentData=parsedJson['data']


        })
}

function check(){

     if(stepsTask){
        currenteResultEndpoit = "stepcheck";
    }
    else {
        currenteResultEndpoit = "encoderesult";
    }

    const url = 'http://localhost:9090/'+currenteResultEndpoit;
    fetch(url,{
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
          },
          body: JSON.stringify({
              'module_name': currentCode,
              'data':currentData,
              'answer': document.getElementById("answer").value,
              'step': steps!=null?steps[currentStep]:'',
          })
        })
        .then( response => {
            console.log(response.status);
            return response.json()
        })
        .then( parsedJson =>{
            console.log(parsedJson);

            document.getElementById('rightAnswer').style.display=' none';
            document.getElementById('wrongAnswer').style.display=' none';

            if(parsedJson['result']){
                document.getElementById('rightAnswer').style.display=' inline-flex';


                 if(stepsTask){
                    if(currentStep===(steps.length-1)){
                        stepsTask = false;
                    }else{
                        currentStep+=1;
                        currentGenerator+=1;
                        beginTest();
                    }
                }
            }
            else{
                document.getElementById('wrongAnswer').style.display=' inline-flex';
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
