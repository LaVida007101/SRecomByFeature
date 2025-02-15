Set objShell = CreateObject("WScript.Shell")

currentDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

outputDirectory = currentDirectory & "\DailyTracks"

' Get the Spotify link passed from the command line argument
Dim spotifyLink
If WScript.Arguments.Count = 0 Then
    WScript.Echo "Error: No Spotify link provided"
    WScript.Quit 1
End If

spotifyLink = WScript.Arguments.Item(0)

' Load environment variables from .env file
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objEnvFile = objFSO.OpenTextFile(".env", 1)

Do Until objEnvFile.AtEndOfStream
    strLine = Trim(objEnvFile.ReadLine)
    If strLine <> "" And InStr(strLine, "=") > 0 Then
        arrPair = Split(strLine, "=")
        key = Trim(arrPair(0))
        value = Trim(arrPair(1))
        
        Select Case key
            Case "CLIENT_ID"
                key = "SPOTIPY_CLIENT_ID"
            Case "CLIENT_SECRET"
                key = "SPOTIPY_CLIENT_SECRET"
            Case "REDIRECT_URI"
                key = "SPOTIPY_REDIRECT_URI"
        End Select
        
        objShell.Environment("Process")(key) = value
    End If
Loop
objEnvFile.Close

objShell.Run "powershell -NoProfile -ExecutionPolicy Bypass -Command ""spotify_dl -mc 3 -l " & spotifyLink & " -o '" & outputDirectory & "'""", 0, True
