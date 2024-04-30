# ⚙️ TOASTER.ACTION-ALERTING-SERVICE

![main_img](https://github.com/STALCRAFT-FUNCKA/toaster.message-handling-service/assets/76991612/8bb6b3bf-8385-4d4b-80cc-e104d5283a9c)

## 📄 Информация
**TOASTER.ACTION-ALERTING-SERVICE** - сервис обработки событий, классифицированных как "запрос на уведомление". Уведомлениями называются все логирующие сообщения, которые отправляются в лог-чаты. Событие приходит от сервиса обработки команд иили сервиса обработки наказаний. Праллельно производятся необходимые действия внутреннего\внешнего логирования.

### Входные данные:
Alert about command call event:
```
{
    "alert_type": "command"
    "user_id":
    "user_name":
    "peer_name":
    "peer_id":
    "command_name":
    "forward":
}
```

Alert about warn initiate event:
```
{
    "alert_type": "warn"
    "user_id":
    "user_name":
    "moderator_name":
    "moderator_id":
    "peer_name":
    "peer_id":
    "warns":
    "total_warns":
    "forward":
}
```

Alert about unwarn initiate event:
```
{
    "alert_type": "unwarn"
    "user_id":
    "user_name":
    "moderator_name":
    "moderator_id":
    "peer_name":
    "peer_id":
    "warns":
    "total_warns":
    "forward":
}
```

Alert about kick event:
```
{
    "alert_type": "kick"
    "user_id":
    "user_name":
    "moderator_name":
    "moderator_id":
    "peer_name":
    "peer_id":
    "forward":
}

```
Пример события, которое приходит от toaster.command-handling-service или toaster.punish-execution-service сервиса на toaster.action-alerting-service.

Далее, сервиc получает из БД список всех чатов, помеченных как "LOG", и отправляет уведомление о событии.

### Дополнительно
Docker stup:
```
docker network
    name: TOASTER
    ip_gateway: 172.18.0.1
    subnet: 172.18.0.0/16
    driver: bridge


docker image
    name: toaster.action-alerting-service
    args:
        TOKEN: "..."
        GROUPID: "..."
        SQL_HOST: "..."
        SQL_PORT: "..."
        SQL_USER: "..."
        SQL_PSWD: "..."


docker container
    name: toaster.action-alerting-service
    network_ip: 172.1.08.11

docker volumes:
    /var/log/TOASTER/toaster.action-alerting-service:/service/logs
```

Jenkins shell command:
```
imageName="toaster.action-alerting-service"
containerName="toaster.action-alerting-service"
localIP="172.18.0.11"
networkName="TOASTER"

#stop and remove old container
docker stop $containerName || true && docker rm -f $containerName || true

#remove old image
docker image rm $imageName || true

#build new image
docker build . -t $imageName \
--build-arg TOKEN=$TOKEN \
--build-arg GROUPID=$GROUPID \
--build-arg SQL_HOST=$SQL_HOST \
--build-arg SQL_PORT=$SQL_PORT \
--build-arg SQL_USER=$SQL_USER \
--build-arg SQL_PSWD=$SQL_PSWD

#run container
docker run -d \
--name $containerName \
--volume /var/log/TOASTER/$imageName:/service/logs \
--restart always \
$imageName

#network setup
docker network connect --ip $localIP $networkName $containerName

#clear chaches
docker system prune -f
```
