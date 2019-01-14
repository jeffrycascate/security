Requisitos
1. Instalar https://download.visualstudio.microsoft.com/download/pr/a2686bb0-bc23-477d-bf8b-28fc39a4fd74/4247ade4aff73f96e390f2576d4d131c/dotnet-sdk-2.2.102-win-x64.exe
2. Instalar https://code.visualstudio.com/docs/editor/extension-gallery
3. https://marketplace.visualstudio.com/items?itemName=ms-vscode.csharp


1. Create folder "Naboo.DataAccess"
2. Ingresar en consola al folder de "Naboo.DataAccess"
    Importante debe quedar target asi <TargetFramework>netcoreapp2.2</TargetFramework>
3. Ingresar el commando "dotnet new classlib"
4. Ingresar al nuget en esta direccion  "https://www.nuget.org/packages/Microsoft.EntityFrameworkCore.Design"
4. Copiar el commando "dotnet add package Microsoft.EntityFrameworkCore.Design --version 2.2.1"
5. Ingresar al nuget en esta direccion  "https://www.nuget.org/packages/Pomelo.EntityFrameworkCore.MySql"
6. Copiar el commando "dotnet add package Pomelo.EntityFrameworkCore.MySql --version 2.1.4"
7. Ingresar al nuget en esta direccion  "https://www.nuget.org/packages/Microsoft.EntityFrameworkCore.Tools"
8. Agregar en el archivo raiz "Naboo.DataAccess.csproj" en el nodo "<ItemGroup>" al final la siguiente linea
    "<DotNetCliToolReference Include="Microsoft.EntityFrameworkCore.Tools" Version="2.2.1" />" (la version dale del url del paso 
    7)
9. Ejecutar commando "dotnet restore"
10. Ejecutar "dotnet ef"
11. Ejecutar "dotnet ef dbcontext scaffold "server=localhost;database=osagnostic;user=root;pwd=Jcv1821@t5" "Pomelo.EntityFrameworkCore.MySql" -o .\Model -f"

Notas:
1.Para inicar es con "dotnet run"
2. para agregar referencia a projecto local es asi 
<ItemGroup>
     <ProjectReference Include="..\Naboo.DataAccess\Naboo.DataAccess.csproj" />
  </ItemGroup>
3. compiar dotnet msbuild

https://www.youtube.com/watch?v=0gHS3U9zMKI