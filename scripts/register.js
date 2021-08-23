async function digestMessage(message) {
    const msgUint8 = new TextEncoder().encode(message);                          
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);           
    const hashArray = Array.from(new Uint8Array(hashBuffer));                    
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join(''); 
    return hashHex;
  }

const escapewords = [".", "/", "<", ">", "="];

const nameform = document.getElementById('name');
const bikouform = document.getElementById('bikou');
const passform = document.getElementById('pass');
const register_button = document.getElementById('register_button');

register_button.addEventListener('click', () => {

    namevalue = nameform.value;
    bikouvalue = bikouform.value;
    passvalue = passform.value;

    if(namevalue != "" && bikouvalue != "" && passvalue != "") {

        try {

            console.log(namevalue);

            if(namevalue.includes('.') || namevalue.includes('/') || namevalue.includes('<') || namevalue.includes('>')) {
                throw new Error('名前に記号は使用できません');
            }

            if(bikouvalue.includes('.') || bikouvalue.includes('/') || bikouvalue.includes('<') || bikouvalue.includes('>')) {
                throw new Error('備考に記号は使用できません');
            }

            digestMessage(passvalue).then(passhash => {

                const register_request = new XMLHttpRequest;

                let formdata = {
                    'name': namevalue,
                    'bikou': bikouvalue,
                    'password': passhash
                };

                register_request.onreadystatechange = function () {

                    if(this.readyState == 4 && this.status == 200) {

                        console.log("リクエスト完了");
                        const div = document.createElement('div');
                        div.innerText = '登録が完了しました。';
                        document.body.appendChild(div)
                        response = this.response;
                        console.log(response);

                    }
                    
                }

                const URL = '/post/user';
                register_request.open('POST', URL, true);
                register_request.setRequestHeader('Content-Type', 'application/json');
                register_request.responseType = 'json';
                register_request.send(JSON.stringify(formdata)); 
            
            });

        }
        catch(e) {

            alert(e.message);
        }       

    }
    else {
        alert('必要な項目を入力してください');
    }

});