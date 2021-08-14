
async function digestMessage(message) {
    const msgUint8 = new TextEncoder().encode(message);                          
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);           
    const hashArray = Array.from(new Uint8Array(hashBuffer));                    
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join(''); 
    return hashHex;
  }

const reference_button = document.getElementById("reference_button");
const message = document.getElementById("msg");

reference_button.addEventListener('click', () => {

    const idbox = document.getElementById("reference_id");
    const passwordbox = document.getElementById("pass");
    const namevalue = idbox.value;
    const passvalue = passwordbox.value;

    if(namevalue != "" && passvalue != "") {

        try {

            //APIによるディレクトリトラバーサル防止
            if(namevalue.includes('.') || namevalue.includes('/')) {
                throw new Error('名前に記号は使用できません');
            }
            
            //入力したパスワードのハッシュ化
            digestMessage(passvalue).then(passhash => {

                const GetUserInforequest = new XMLHttpRequest;
                let formdata = {
                    'name' : namevalue,
                    'password' : passhash
                };
        
                GetUserInforequest.onreadystatechange = function () {

                    if(this.readyState == 4 && this.status == 200) {

                        const response = this.response;
                        console.log(response)
                        let div = document.createElement('div');
                        div.innerText = '名前: ' + response.user_info[0].name + '備考: ' + response.user_info[0].bikou;
                        document.body.appendChild(div);

                    } else if(this.readyState == 4 && this.status == 401) {

                        const response = this.response.detail;
                        alert(response);

                    }
                }
                const URL = '/get/user/info';
                GetUserInforequest.open('POST', URL, true);
                GetUserInforequest.setRequestHeader('Content-Type', 'application/json');
                GetUserInforequest.responseType = 'json';
                GetUserInforequest.send(JSON.stringify(formdata));

            });
            
        }
        catch(e) {

            alert(e.message);

        }

    }
    else if(idvalue == "" && passvalue == "") {
        alert('IDとパスワードを入力してください');
    }
    else if(idvalue == "") {
        alert('IDを入力してください');
    }
    else {
        alert('パスワードを入力してください');
    }
});