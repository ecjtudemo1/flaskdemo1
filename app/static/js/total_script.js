
window.onload = function () {
var check = document.getElementById("check_mail");
var check_num = check.innerHTML;//js来获取html中的内容和数据
//alert(check);//如何获取html中的数据
var text = document.getElementById("11111");
    text.style.color='red';
    if (check_num == 1){
        alert("邮件已发送成功");
    }
    else if(check_num == 0){
        alert("邮件发送失败");
    }
    //function change() {
        //var ddd = document.body;
        //var dddd = document.getElementById("jstext");
        //ddd.style.background="url('../bgp111.jpg')";
        //dddd.style.background= url('../smj.jpg');
    //}
     //setInterval(change, 1000);//背景的轮播      未解决？？？？？？？？？？？？？？？？？？？

};

