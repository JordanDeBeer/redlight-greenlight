package lambdaServer

import (
	"github.com/aws/aws-lambda-go/events"
)

type Response events.APIGatewayProxyResponse

func Handler(context events.APIGatewayWebsocketProxyRequestContext, request events.APIGatewayWebsocketProxyRequest) (Response, error) {
	return Response{StatusCode: 200, Body: "OK"}, nil
}
