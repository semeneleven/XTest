
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

onlyEncode = false;
encode = false;
decode = false;

isExam = false;
currentAnswer = null;
currentExamTask = 0;
examTasks = 0;
rightExamAnswers = 0;

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

            console.log(parsedJson['codes']);

            Object.keys(parsedJson['codes']).forEach(function (code) {
                div = document.createElement('div');
                par = document.createElement('p');

                if(this.color === 0){
                    div.classList.add('code-plate-1')
                }else {
                    div.classList.add('code-plate-2')
                }
                this.color = (this.color + 1)%2;

                div.id = code;
                div.onclick = (ev) => {

                    getCodeDetails(ev.target.id)
                };

                par.classList.add('main-text');
                par.innerText = parsedJson['codes'][code];

                div.appendChild(par);
                this.codesDiv.appendChild(div)
            })
            this.codesDiv.style.display = 'flex'
        })

}

function getCodeDetails(codeName) {

    document.getElementById("codes").style.display = 'none';
    isExam = false;

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

            onlyEncode = false;
            encode = false;
            decode = false;
            stepsTask = false;
            waitResponse=false;

            console.log(parsedJson);
            this.codeDiv = document.getElementById("code");
            this.codeDiv.style.display = 'flex';
            this.theory= document.getElementById("theory");
            clear(this.theory);
            this.theory.innerHTML = parsedJson['description'];

            if(parsedJson["details"]["only_encode"] !== undefined&&parsedJson["details"]["only_encode"]===true){
                onlyEncode = true;
            }

            if(parsedJson["details"]["generators"] !== undefined){
                generators = parsedJson["details"]["generators"];
                steps = parsedJson["details"]["steps"];
                stepsTask = true;
                currentGenerator = 0;
                currentStep = 0;
            }

            currentCode = codeName;

        })
}


function showModal(){

    if(onlyEncode)
        beginEncode();
    else {
        var modal = document.getElementById('modalWindow');
        modal.style.display = 'block';
        window.onclick = function (event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        }
    }

}

function beginEncode() {

    encode = true;
    currentAnswer = null;

    document.getElementById('modalWindow').style.display=' none';

    document.getElementById('rightAnswer').style.display=' none';
    document.getElementById('wrongAnswer').style.display=' none';

    if(currentCode===''&&!waitResponse) {
        waitResponse=true;
        setTimeout(beginEncode, 100);
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



function beginDecode() {

    decode = true;
    currentAnswer = null;

    document.getElementById('modalWindow').style.display=' none';

    document.getElementById('rightAnswer').style.display=' none';
    document.getElementById('wrongAnswer').style.display=' none';

    if(currentCode===''&&!waitResponse) {
        waitResponse=true;
        setTimeout(beginEncode, 100);
    }

    document.getElementById("code").style.display = 'none';

    currenteEncoderEndpoit = "decodedata";


    const url = 'http://localhost:9090/'+currenteEncoderEndpoit;
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
            currentData=parsedJson['data']


        })
}

function showResultModal(){

    if(onlyEncode)
        beginEncode();
    else {
        var modal = document.getElementById('modalResultWindow');
        var resultTextParagraph = document.getElementById('resultText');
        var resultParagraph = document.getElementById('result');
        resultTextParagraph.innerText = "Вірних відповідей: " + rightExamAnswers +" из " + examTasks;
        resultParagraph.innerText = "Оцінка: " + (rightExamAnswers/examTasks*100).toFixed(1);
        modal.style.display = 'block';  
        window.onclick = function (event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        }
    }

}

async function check() {

    if (encode)
        currentAnswer = await checkEncode();
    if (decode)
        currentAnswer = await checkDecode();

    console.log(isExam, currentAnswer, currentExamTask, examTasks);

    if (isExam) {
        if (currentAnswer) {
            document.getElementById("answered" + currentExamTask).classList.add('true-answered');
            rightExamAnswers +=1;
        }
        else
            document.getElementById("answered" + currentExamTask).classList.add('false-answered');

        currentExamTask += 1;
        if(stepsTask){
            if(currentStep === (steps.length - 1)){
                stepsTask = false;
                isExam = false;
                goBack();
                showResultModal();
                return
            }else{
                 currentStep += 1;
                 currentGenerator += 1;
                 beginEncode();
            }
        }else {

            if (currentExamTask === examTasks) {
                isExam = false;
                onlyEncode = false;
                goBack();
                showResultModal();
                return
            }


            if (currentExamTask < examTasks / 2 && !stepsTask||onlyEncode)
                beginEncode();
            else
                beginDecode();
        }
    }
}


async function checkEncode() {
    if (stepsTask) {
        currenteResultEndpoit = "stepcheck";
    }
    else {
        currenteResultEndpoit = "encoderesult";
    }

    var answersRequest = null;
    answers = document.getElementsByName("answer");

    if (answers.length === 1)
        answersRequest = answers[0].value;
    else {
        answersRequest = new Array();
        for (var answer of answers) {
            answersRequest.push(answer.value)
        }
    }

    const url = 'http://localhost:9090/' + currenteResultEndpoit;
    return await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            'module_name': currentCode,
            'data': currentData,
            'answer': answersRequest,
            'step': steps != null ? steps[currentStep] : '',
        })
    })
        .then(response => {
            console.log(response.status);
            return response.json()
        })
        .then(parsedJson => {
            console.log(parsedJson);

            document.getElementById('rightAnswer').style.display = ' none';
            document.getElementById('wrongAnswer').style.display = ' none';

            currentAnswer = parsedJson['result'];

            if(!isExam){

                if (parsedJson['result']) {
                    document.getElementById('rightAnswer').style.display = ' inline-flex';


                    if (stepsTask) {

                        if (currentStep === (steps.length - 1)) {
                            stepsTask = false;
                        } else {
                            currentStep += 1;
                            currentGenerator += 1;
                            beginEncode();
                        }
                    }
                }
                else {
                    document.getElementById('wrongAnswer').style.display = ' inline-flex';
                }
            }
            return parsedJson['result']
        })
}

async function checkDecode() {

    currenteResultEndpoit = "decoderesult";

    var answersRequest = null;
    answers = document.getElementsByName("answer");

    if(answers.length===1)
        answersRequest = answers[0].value;
    else {
        answersRequest = new Array();
        for(var answer of answers){
            answersRequest.push(answer.value)
        }
    }

    const url = 'http://localhost:9090/'+currenteResultEndpoit;
    return await fetch(url,{
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
          },
          body: JSON.stringify({
              'module_name': currentCode,
              'data':currentData,
              'answer': answersRequest,
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

            currentAnswer = parsedJson['result'];

            if(!isExam) {

                if (parsedJson['result']) {
                    document.getElementById('rightAnswer').style.display = ' inline-flex';
                }
                else {
                    document.getElementById('wrongAnswer').style.display = ' inline-flex';
                }
            }

            return parsedJson['result'];
        })
}


function startExam(){
    isExam = true;
    rightExamAnswers = 0;

    if(currentCode===''&&!waitResponse) {
        waitResponse=true;
        setTimeout(beginEncode, 100);
    }

    var exam = document.getElementById("exam");

    const url = 'http://localhost:9090/exam';
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
            console.log(parsedJson['view']);
            exam.innerHTML = parsedJson['view'];
            examTasks = parsedJson['exam_tasks'];
        });

    document.getElementById("code").style.display = 'none';
    exam.style.display = 'flex';
    currentExamTask = 0;
    beginEncode()
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
        document.getElementById("exam").style.display='none';
        document.getElementById("bottom").style.display = 'flex';
        currentData='';
        getCodeDetails(currentCode)
    }

}

function clear(div) {
    div.innerHTML = ''
}
