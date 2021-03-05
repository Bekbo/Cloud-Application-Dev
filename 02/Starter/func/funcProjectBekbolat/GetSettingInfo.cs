using Microsoft.Azure.WebJobs;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
namespace funcProjectBekbolat
{
    public static class GetSettingInfo
    {
        [FunctionName("GetSettingInfo")]
        public static IActionResult Run([HttpTrigger("GET")] HttpRequest request,[Blob("content/settings.json")] string json)=> new OkObjectResult(json);

    }
}
