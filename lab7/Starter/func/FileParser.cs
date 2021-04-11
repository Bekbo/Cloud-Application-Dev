using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.AspNetCore.Http;
using Azure.Storage.Blobs;

namespace func
{
    public static class FileParser{
        [FunctionName("FileParser")]
        public static async Task<IActionResult> Run([HttpTrigger("GET")] HttpRequest request){
            string connectionString = Environment.GetEnvironmentVariable("StorageConnectionString");
            BlobClient blob = new BlobClient(connectionString, "drop", "records.json");
            var response = await blob.DownloadAsync();
            return new FileStreamResult(response?.Value?.Content, response?.Value?.ContentType);
        }

    }

    // public static class FileParser
    // {
    //     [FunctionName("FileParser")]
    //     public static async Task<IActionResult> Run(
    //         [HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)] HttpRequest req,
    //         ILogger log)
    //     {
    //         log.LogInformation("C# HTTP trigger function processed a request.");

    //         string name = req.Query["name"];

    //         string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
    //         dynamic data = JsonConvert.DeserializeObject(requestBody);
    //         name = name ?? data?.name;

    //         string responseMessage = string.IsNullOrEmpty(name)
    //             ? "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response."
    //             : $"Hello, {name}. This HTTP triggered function executed successfully.";

    //         return new OkObjectResult(responseMessage);
    //     }
    // }
}
