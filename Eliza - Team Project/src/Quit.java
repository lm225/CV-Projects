import java.io.*;
import java.util.Random;


public class Quit {

	public boolean endProgram(String[] words) throws IOException{

		boolean output = false;
		try{
			BufferedReader reader = new BufferedReader(new FileReader(
					"script.txt"));
			String quitWords;
			String response;

			for(int i = 0; i < words.length; i ++){
				//read each line of the script (to the end)
				while ((quitWords = reader.readLine()) != null) {
					//check that the first character of the line is a 7
					if (quitWords.charAt(0) == ('7')) {
						//array to contain the words of each line in the script
						String[] quitCommands = quitWords.split("::");

						//check that the current word array element equals the second response array element
						if (words[i].equals(quitCommands[1])) {

							//a second loop to look through the script again...
							while((response = reader.readLine()) != null){
								//...to find a different character
								if (response.charAt(0) == ('8')) {
									//an array to include the possible responses
									String[] foundResponse = response.split("::");

									//generate a random number to give a random response
									int r = 0;
									while(r < 1){
										Random random = new Random();
										r = random.nextInt(foundResponse.length);
									}
									System.out.println(foundResponse[r]);
									output=true;


								}

							}
						}
					}
				}

			}
		}

		catch(FileNotFoundException e){
			System.out.println("The File Specified Could Not Be Found");
		}

		return output;



	}




}	
