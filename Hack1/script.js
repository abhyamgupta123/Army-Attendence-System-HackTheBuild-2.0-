const baseUrl="http://192.168.43.182:8000/"


const handleScanRegistration=()=>{
    document.querySelector("#regbody").style.display="none"
    document.querySelector("#regsyc").style.display="grid"
}

const changePasswordView=(x)=>{
   let inputType=x.parentElement.firstElementChild;
   inputType.type=inputType.type==="text"?"password":"text"
}

const handleMarkAttendance=()=>{
    document.querySelector(".markYourAttendance").style.display="none"
    document.querySelector(".scanYourCard").style.display="grid"
    $.ajax({
        url: `${baseUrl}attendence/recordAttendence`,
        type: 'POST',
        success:function (res){
               $("#syc").css("display","none")
               $("#smc").css("display","grid");
               console.log(res)
             },
        error:function(res){
            console.log(res)
            $("#syc").css("display","none")
            $("#errmya").css("display","grid")
            $("#errmyamsg").html(res.responseJSON.error)
        }
    })
}

const handleRegisterNext=()=>{
    try{
        const loginName=document.getElementById("userReg").value
        const email=document.getElementById("emailReg").value
        const loginpass=document.getElementById("passReg").value
        const confirmloginpass=document.getElementById("passcReg").value
        $("#regbody").css("display","none")
        $("#regsyc").css("display","grid");

        console.log(loginName,email,loginpass,confirmloginpass,"amanpratapsingh")
        $.ajax({
            url: `${baseUrl}user/register`,
            type: 'POST',
            data:{
              loginName,email,loginpass,confirmloginpass
            },
            success:function (res){
                   console.log(res)
                   $("#regsyc").css("display","none");
                   $("#regres").css("display","grid");

                 },
            error:function(res){
                console.warn(res.responseJSON.error)
                alert(res.responseJSON.error)            
            }
        })
    }
    catch(e){
        console.log(e)
    }
}

const handleRegisterNext2=()=>{
    const loginName=document.getElementById("userLog").value
    const loginpass=document.getElementById("passLog").value
    $.ajax({
        url: `${baseUrl}user/register`,
        type: 'POST',
        data:{
          loginNam,loginpass
        },
        success:function (res){
               $("#syc").css("display","none")
               $("#smc").css("display","grid");
               console.log(res)
             },
        error:function(res){
            alert("There was some error while marking your attendance "+res)
        }
    })
}

const handleDeleteUser=()=>{
    const username=$("#userDel").val()
    // const loginpass=$("#userDel").val()
    console.log("yoyoyo",username)
    $("#delbody").css("display","none")
    $("#delsyc").css("display","grid");

    $.ajax({
        url:  `${baseUrl}user/deleteUser`,
        type: 'POST',
        data:{
          username,
        },
        success:function (res){
               $("#delbody").css("display","none")
               $("#delres").css("display","grid");
               console.log(res)
             },
        error:function(res){
            alert(res.responseJSON.error)
        }
    })
}

const handleFormatCard=(url)=>{
    // const loginpass=$("#userDel").val()
    console.log("yoyoyo")
    $("#forbody").css("display","none")
    $("#forsyc").css("display","grid");

    $.ajax({
        url: `${baseUrl}attendence/${url}`,
        type: 'POST',
        success:function (res){
               $("#forsyc").css("display","none")
               $("#forres").css("display","grid");
               $("#forresttext").html(res)
             },
        error:function(res){
            alert(res.responseJSON.error)
        }
    })
}


const handleAllAttendance=()=>{

    $("#vttsyc").css("display","grid");

    $.ajax({
        url:  `${baseUrl}attendence/calculateAttendence`,
        type: 'POST',
        success:function (res){
            console.log(res)

               $("#vttsyc").css("display","none")
               $("#forrestext").append(`<h2>${res.Username}</h2><p style="margin-bottom:2rem">${res.Email}</p>`)
                for (const key in res.data) {
                    $("#forrestext").append(`<div class="individualDayDiv"><span>Day ${key}</span><span>${res.data[key]==="1"?"Present":"Absent"}</div>`)
                }
             },
        error:function(res){
            alert(res.responseJSON.error)
        }
    })
}


const handleLogin=()=>{
    $("#vttsyc").css("display","grid");
    $.ajax({
        url:  `${baseUrl}token/`,
        type: 'POST',
        data:{
            username:$("#userLog").val(),
            password:$("#passLog").val()
        },
        success:function (res){
                localStorage.setItem("token",res.access)
                window.location.href=res.admin==true?'./admindashboard.html':'./dashboard.html'
             },
        error:function(res){
            console.log(res.responseJSON.error,res.responseJSON.detail)
            alert(res.responseJSON.error)
        }
    })
}


const getInfoDashboard=()=>{

 console.log(localStorage.getItem("token"))
    $.ajax({
        url:  `${baseUrl}user/adminpanel`,
        type: 'get',
        headers:{
            Authorization:`Bearer ${localStorage.getItem("token")}`
        },
        success:function (res){
                console.log(res)
                $("#headingDB").append(`<h2>${res.username}</h2>`)
                
                for (const key in res.data) {
                    $("#subtitleDB").append(`<h1>${key}</h1>`)
                    for(const key2 in res.data[key]){
                        $("#bodyDB").append(`<div class="individualDayDiv"><span>Day ${res.data[key2]}</span><span>${res.data[key][key2]}</div>`)
                    }
                    // $("#body").append(`<div class="individualDayDiv"><span>Day ${key}</span><span>${res.data[key]}</div>`)
                }
             },
        error:function(res){
            console.log(res)
            alert(res.responseJSON.error)
        }
    })
}

const getInfoAdminDashboard=()=>{

    console.log(localStorage.getItem("token"))
       $.ajax({
           url:  `${baseUrl}user/adminpanel`,
           type: 'get',
           headers:{
               Authorization:`Bearer ${localStorage.getItem("token")}`
           },
           success:function (res){
                   console.log(res)
                   $("#headingDB").append(`<h2>${res.username}</h2>`)
                   
                   for (const key in res.data) {
                       $("#subtitleDB").append(`<h1>User ${key}</h1>`)
                       for(const key2 in res.data[key]){
                           $("#bodyDB").append(`<span class="individualDayDiv">Day ${key2}</span><br/><br/>`)
                           for(const key3 in res.data[key][key2]){
                               $("#attDB").append(`<span style="margin:0.25rem;background:${res.data[key][key2][key3]==1?"aquamarine":"transparent"};color:${res.data[key][key2][key3]==1&&"black"}">${res.data[key][key2][key3]==1?"P":"A"}&nbsp;</span>`)
                           }
                       }
                       // $("#body").append(`<div class="individualDayDiv"><span>Day ${key}</span><span>${res.data[key]}</div>`)
                   }
                },
           error:function(res){
               console.log(res)
               // alert(res.responseJSON.error)
           }
       })
   }