let card = NaN
const csrftoken = getCookie("csrftoken");
let target_id = 0

function allowDrop(ev){
    ev.preventDefault();
}

function drag(ev){
    ev.dataTransfer.setData("text", ev.target.dataset.id)
    card = ev.target
    return target_id = ev.target.dataset.id
}

function drop(ev){
    ev.preventDefault();
    fetch(`/project/task-status-change/`, {
        credentials: "include",
        method: "POST",
        mode: "same-origin",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
            task_id: target_id,
            new_status: ev.target.dataset.status,
        }),
    })
    .then((response) => response.json())
    .then((response) => {
        if(response.message == "Task status changed"){
            ev.target.appendChild(card);
        }
    })
    
}

// fetch(`/profiles/profile/follow_user/`, {
//     credentials: "include",
//     method: "POST",
//     mode: "same-origin",
//     headers: {
//       Accept: "application/json",
//       "Content-Type": "application/json",
//       "X-CSRFToken": csrftoken,
//     },
//     body: JSON.stringify({
//       following_user: user_id,
//     }),
//   })
//     .then((response) => response.json())
//     .then((follow) => {
//       if(followBtn.innerText == "FOLLOW"){
//         number++
//         if(number == 1){
//           total_followers.innerHTML = `${number} obserwujący`
//         }else{
//           total_followers.innerHTML = `${number} obserwujących`
//         }
//         followBtn.innerText = "UNFOLLOW"
//       }
//       else{
//         number--
//         if(number == 1){
//           total_followers.innerHTML = `${number} obserwujący`
//         }else{
//           total_followers.innerHTML = `${number} obserwujących`
//         }
//         followBtn.innerText = "FOLLOW"
        
//       }
//     });
// });
// }



// });

// def user_follow(request):
//     user = Profile.objects.get(id=request.user.id)
//     following_user = json.loads(request.body.decode("UTF-8"))
//     following_user_id = following_user['following_user']
//     follow = Profile.objects.get(id=following_user_id)
//     is_following = UserFollows.objects.filter(
//         user_id=follow, following_user_id=user)
//     if request.method == "POST":
//         if is_following.exists():
//             is_following.delete()
//             return JsonResponse({'message': 'Już nie obserwujesz tej osoby.'}, status=201)
//         else:
//             UserFollows.objects.create(user_id=follow, following_user_id=user)
//             create_action(request.user, "Obserwuje", follow)
//             return JsonResponse({'message': 'Obserwujesz tą osobę.'}, status=201)
//     return JsonResponse({'message': 'Obserwujesz tą osobę.'})
