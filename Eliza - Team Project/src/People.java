import java.io.*;
import java.util.Random;

public class People {

	public boolean findPeople(String[] words) throws IOException{

		boolean output = false;
		try{
			BufferedReader reader = new BufferedReader(new FileReader(
					"script.txt"));
			String people;
			String response;

			//read each line of the script (to the end)
			while ((people = reader.readLine()) != null) {
				for(int i = 0; i < words.length; i ++){
					//check that the first character of the line is a 3
					if (people.charAt(0) == ('3')) {
						//array to contain the words of each line in the script
						String[] foundPeople = people.split("::");

						//check that the current word array element is equal to the second foundPeople array element
						if (words[i].equals(foundPeople[1])) {


							//a second loop to look through the script again...
							while((response = reader.readLine()) != null){
								//...to find a different character
								if (response.charAt(0) == ('4')) {
									//array to contain the possible responses
									String[] foundResponse = response.split("::");
									//generate a random number to give a random response
									int r = 0;
									while(r < 2){
										Random random = new Random();
										r = random.nextInt(foundResponse.length);
									}
									System.out.println(foundResponse[r] + foundPeople[1] + "?");
									output = true;
									return output;
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