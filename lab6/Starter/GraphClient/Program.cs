using Microsoft.Identity.Client;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Graph;
using Microsoft.Graph.Auth;
namespace GraphClient
{
    class Program
    {
        private const string _clientId = "28238244-13ca-4d39-b682-9e4494658f4a";
        private const string _tenantId = "57081b5e-e66a-4993-8eaf-15b0b309293f";
        public static async Task Main(string[] args){
            IPublicClientApplication app = PublicClientApplicationBuilder
            .Create(_clientId)
            .WithAuthority(AzureCloudInstance.AzurePublic, _tenantId)
            .WithRedirectUri("http://localhost")
            .Build();
            List<string> scopes = new List<string>{ "user.read"};
            // AuthenticationResult result;
            // result = await app
            // .AcquireTokenInteractive(scopes)
            // .ExecuteAsync();
            // Console.WriteLine($"Token:\t{result.AccessToken}");

            DeviceCodeProvider provider = new DeviceCodeProvider(app, scopes);
            GraphServiceClient client = new GraphServiceClient(provider);
            User myProfile = await client.Me
            .Request()
            .GetAsync();
            Console.WriteLine($"Name:\t{myProfile.DisplayName}");
            Console.WriteLine($"AAD Id:\t{myProfile.Id}");
        }
    }
}