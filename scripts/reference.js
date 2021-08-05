
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
    const idvalue = idbox.value;
    const passvalue = passwordbox.value;

    if(idvalue != "" && passvalue != "") {

        try {

            //ディレクトリトラバーサル防止
            if(idvalue.includes('.') || idvalue.includes('/')) {
                throw new Error('名前に記号は使用できません');
            }
            
            //入力したパスワードのハッシュ化
            digestMessage(passvalue).then(passhash => {
                console.log(passhash);
                const PassCheckrequest = new XMLHttpRequest;
        
                PassCheckrequest.onreadystatechange = function () {

                    if(this.readyState == 4 && this.status == 200) {

                        const response = this.response;
                        const anshash = response.user_pass[0].pass;

                        if(passhash == anshash) {

                            const request = new XMLHttpRequest();
                            request.onreadystatechange = function() {
                                if(this.readyState == 4 && this.status == 200) {
                                    console.log('DONE:リクエスト完了');
                                    const responses = this.response;
                                    let div = document.createElement('div');
                                    div.innerText = '名前: ' + responses.id_user[0].name + '  備考: ' + responses.id_user[0].bikou;
                                    document.body.appendChild(div);
                                }
                            }
                            const URL = '/get/user/' + idvalue;
                            request.open('GET', URL, true);
                            request.responseType = 'json';
                            request.send();    
                        }
                        else {
                            alert('パスワードが違います。');
                        }

                    }
                }
                const pcURL = 'get/user/' + idvalue + '/pass';
                PassCheckrequest.open('GET', pcURL, true);
                PassCheckrequest.responseType = 'json';
                PassCheckrequest.send();

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