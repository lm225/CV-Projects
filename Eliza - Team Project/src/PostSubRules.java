import java.io.*;
import java.util.Random;

public class PostSubRules {

	public boolean postSubRules(String[] words, int i ) {

		boolean output = false;
		try {
			BufferedReader reader = new BufferedReader(new FileReader(
					"script.txt"));
			String subRules;

			//read each line of the script (to the end)
			while ((subRules = reader.readLine()) != null) {
				//check that the first character of the line is a 1
				if (subRules.charAt(0) == ('1')) {
					//array to contain the words of each line in the script
					String[] response = subRules.split("::");

					//check that the current word array element equals the second response array element
					if (words[i].equals(response[1])) {
						output = true;
						//generate a random number to give a random response
						int r = 0;
						while(r < 2){
							Random random = new Random();
							r = random.nextInt(response.length);
						}
						System.out.print(response[r] + " ");

					}
				}
			}

		} catch (FileNotFoundException e) {
			System.out.println("The File Specified Could Not Be Found");
		} catch (IOException e) {
			System.out.println("IO Exception Has Been Made");
		}
		return output;

	}
}
