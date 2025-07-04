"use client"

import * as React from "react"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import { CheckIcon } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { useToast } from "@/hooks/use-toast"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useRegionalCurrency } from "@/hooks/use-currency"

const formSchema = z.object({
  email: z.string().email({ message: "Please enter a valid email address." }),
  option: z.enum(["waitlist", "reserve"]),
})

type EarlyAccessFormValues = z.infer<typeof formSchema>

export function EarlyAccessDialog({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = React.useState(false)
  const [showPayment, setShowPayment] = React.useState(false)
  const { toast } = useToast()
  const { display } = useRegionalCurrency();

  const form = useForm<EarlyAccessFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
      option: "waitlist",
    },
  })

  const watchOption = form.watch("option")

  React.useEffect(() => {
    setShowPayment(watchOption === "reserve")
  }, [watchOption])

  function onSubmit(data: EarlyAccessFormValues) {
    console.log("Early access request:", data)
    toast({
      title: "Success!",
      description: data.option === "reserve" 
        ? "Your spot has been reserved! Payment processed successfully." 
        : "You've been added to our early access list.",
    })
    form.reset()
    setIsOpen(false)
    setShowPayment(false)
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="sm:max-w-lg rounded-xl bg-gradient-to-br from-gray-900 to-gray-800 border-gray-700">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            🚀 — Join our Early Access list
          </DialogTitle>
        </DialogHeader>
        
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-gray-300">Email</FormLabel>
                  <FormControl>
                    <Input
                      className="bg-gray-800 border-gray-700 text-white placeholder:text-gray-500 focus:ring-2 focus:ring-blue-500"
                      placeholder="name@example.com"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-300">
                Want Priority Access?
              </h3>
              
              <FormField
                control={form.control}
                name="option"
                render={({ field }) => (
                  <FormItem className="space-y-3">
                    <FormControl>
                      <RadioGroup
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                        className="grid grid-cols-1 gap-4"
                      >
                        <FormItem className="flex items-start space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem 
                              value="waitlist" 
                              className="text-blue-500 border-gray-600 focus:ring-2 focus:ring-blue-500"
                            />
                          </FormControl>
                          <FormLabel className="font-normal text-gray-300 cursor-pointer">
                          <span className="font-medium text-white">Join free waitlist</span>
                            <div className="flex items-center text-gray-300 text-sm mt-1">
                              <CheckIcon className="w-4 h-4 text-green-400 mr-2" />
                              20% Discount when we launch
                            </div>
                          </FormLabel>
                        </FormItem>
                        
                        <FormItem className="flex items-start space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem 
                              value="reserve" 
                              className="text-blue-500 border-gray-600 focus:ring-2 focus:ring-blue-500"
                            />
                          </FormControl>
                          <div className="flex-1">
                            <FormLabel className="font-normal text-gray-300 cursor-pointer">
                              <div className="flex justify-between items-start">
                                <div>
                                  <span className="font-medium text-white">Reserve your spot</span>
                                  <span className="ml-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white text-xs font-bold px-2 py-1 rounded-full">
                                  {display} (fully refundable)
                                  </span>
                                </div>
                                <div className="bg-gradient-to-r from-yellow-600 to-yellow-800 text-yellow-100 text-xs font-bold px-2 py-1 rounded">
                                  LIMITED TIME
                                </div>
                              </div>
                              <div className="mt-2">
                                <div className="flex items-center text-gray-300 text-sm mt-1">
                                  <CheckIcon className="w-4 h-4 text-green-400 mr-2" />
                                  50% Lifetime Discount
                                </div>
                                <div className="flex items-center text-gray-300 text-sm mt-1">
                                  <CheckIcon className="w-4 h-4 text-green-400 mr-2" />
                                  Free Trial When We Launch
                                </div>
                                <div className="flex items-center text-gray-300 text-sm mt-1">
                                  <CheckIcon className="w-4 h-4 text-green-400 mr-2" />
                                  First-in-Line Product Access
                                </div>
                              </div>
                            </FormLabel>
                          </div>
                        </FormItem>
                      </RadioGroup>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            
            {showPayment && (
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-300">Payment Information</h3>
                
                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader className="pb-3">
                    <CardTitle className="flex justify-between items-center text-gray-300">
                      <span>Payment Amount</span>
                      <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                        $10.00 USD
                      </span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <FormLabel className="text-gray-400">Card Number</FormLabel>
                      <Input
                        className="bg-gray-700 border-gray-600 text-white placeholder:text-gray-500"
                        placeholder="1234 5678 9012 3456"
                      />
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <FormLabel className="text-gray-400">Expiry Date</FormLabel>
                        <Input
                          className="bg-gray-700 border-gray-600 text-white placeholder:text-gray-500"
                          placeholder="MM/YY"
                        />
                      </div>
                      <div>
                        <FormLabel className="text-gray-400">CVC</FormLabel>
                        <Input
                          className="bg-gray-700 border-gray-600 text-white placeholder:text-gray-500"
                          placeholder="123"
                        />
                      </div>
                    </div>
                    
                    <div className="flex items-center text-sm text-gray-400">
                      <CheckIcon className="w-4 h-4 text-green-400 mr-2" />
                      Fully refundable at any time before launch
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
            
            <Button 
              type="submit"
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-3 rounded-lg transition-all duration-300 transform hover:scale-[1.02] shadow-lg"
            >
              {showPayment ? "Reserve Your Spot" : "Join Early Access"}
            </Button>
            
            <p className="text-center text-xs text-gray-500">
              By joining, you agree to our Terms and Privacy Policy. Your $10 reservation is fully refundable at any time before launch.
            </p>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}